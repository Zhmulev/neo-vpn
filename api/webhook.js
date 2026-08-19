export default async function handler(req, res) {
  const { path } = req.query;
  const baseUrl = 'http://91.132.57.27:8000';
  
  // Если path не указан — это webhook от ЮKassa
  const url = path ? `${baseUrl}${path}` : `${baseUrl}/pay/webhook`;

  try {
    const response = await fetch(url, {
      method: req.method,
      headers: { 'Content-Type': 'application/json' },
      body: req.method === 'POST' ? JSON.stringify(req.body) : undefined
    });

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}