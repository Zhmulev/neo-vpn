import hmac
import hashlib
import uuid
import logging
from app.core.config import settings
from app.models.payment import PaymentTransaction, PaymentStatus
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class PaymentService:
    @staticmethod
    def create_payment_link(user_id: int, amount: float, db: Session) -> dict:
        """Создает транзакцию и возвращает ссылку на оплату"""
        external_id = str(uuid.uuid4())

        transaction = PaymentTransaction(
            user_id=user_id,
            amount=amount,
            external_id=external_id,
            status=PaymentStatus.PENDING
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        # Формируем ссылку на оплату (имитация платежного шлюза)
        payment_url = f"{settings.PAYMENT_BASE_URL}/pay?shop={settings.PAYMENT_SHOP_ID}&order={external_id}&amount={amount}"

        return {
            "payment_url": payment_url,
            "transaction_id": transaction.id,
            "external_id": external_id
        }

    @staticmethod
    def verify_webhook_signature(payload: dict, signature: str) -> bool:
        """Проверяет HMAC SHA256 подпись от платежного шлюза"""
        if not settings.PAYMENT_WEBHOOK_SECRET:
            logger.warning("PAYMENT_WEBHOOK_SECRET is not set!")
            return False

        # Сортируем ключи и формируем строку для подписи
        sorted_keys = sorted(payload.keys())
        data_string = "&".join([f"{k}={payload[k]}" for k in sorted_keys])

        expected_signature = hmac.new(
            settings.PAYMENT_WEBHOOK_SECRET.encode('utf-8'),
            data_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    @staticmethod
    def process_webhook(external_id: str, amount: float, db: Session) -> bool:
        """Обрабатывает успешную оплату"""
        from app.models.user import User

        transaction = db.query(PaymentTransaction).filter(
            PaymentTransaction.external_id == external_id
        ).first()

        if not transaction:
            logger.error(f"Transaction {external_id} not found")
            return False

        if transaction.status == PaymentStatus.PAID:
            logger.info(f"Transaction {external_id} already processed")
            return True

        if abs(transaction.amount - amount) > 0.01:
            logger.error(f"Amount mismatch for {external_id}: expected {transaction.amount}, got {amount}")
            transaction.status = PaymentStatus.FAILED
            db.commit()
            return False

        # Начисляем баланс
        user = db.query(User).filter(User.id == transaction.user_id).first()
        if not user:
            logger.error(f"User {transaction.user_id} not found")
            return False

        user.balance += amount
        transaction.status = PaymentStatus.PAID
        db.commit()

        logger.info(f"Successfully topped up {amount} for user {user.id}")
        return True