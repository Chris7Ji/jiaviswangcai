export default async function handler(req, res) {
  // CORS configuration
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const FEISHU_APP_ID = process.env.FEISHU_APP_ID;
  const FEISHU_APP_SECRET = process.env.FEISHU_APP_SECRET;
  const FEISHU_BITABLE_TOKEN = process.env.FEISHU_BITABLE_TOKEN; // The base token KyQRbylK9aGWoHscgFJcfHtonQc
  const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;

  if (req.method === 'POST') {
    const { name, content } = req.body;
    
    if (!name || !content) {
      return res.status(400).json({ status: 'error', message: 'Name and content are required' });
    }

    try {
      // 1. AI Review (DeepSeek)
      let status = 'PASS';
      try {
        const aiRes = await fetch('https://api.deepseek.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
          },
          body: JSON.stringify({
            model: 'deepseek-chat',
            messages: [
              { role: 'system', content: 'You are a moderation AI. Review the following guestbook message. If it contains any offensive, hateful, sexual, spam, or politically sensitive content, reply with "REJECT". Otherwise, reply with "PASS". Do not explain, output strictly 1 word.' },
              { role: 'user', content: `Message from ${name}: ${content}` }
            ]
          })
        });
        
        if (aiRes.ok) {
          const aiData = await aiRes.json();
          const decision = aiData.choices[0].message.content.trim().toUpperCase();
          if (decision.includes('REJECT')) status = 'REJECT';
        }
      } catch (err) {
        console.error("AI review failed, defaulting to PASS", err);
      }

      // 2. Feishu Token
      let tenantToken = '';
      try {
        const tokenRes = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ app_id: FEISHU_APP_ID, app_secret: FEISHU_APP_SECRET })
        });
        const tokenData = await tokenRes.json();
        tenantToken = tokenData.tenant_access_token;
      } catch (err) {
        console.error("Failed to get Feishu token", err);
        return res.status(500).json({ status: 'error', message: 'Database auth failed' });
      }

      // 3. Write to Bitable
      // We will read the table ID dynamically or hardcode it since we know it.
      // Current table_id is tbl9cpBHOK7dB4BG
      try {
        const now = new Date().toISOString();
        const writeRes = await fetch(`https://open.feishu.cn/open-apis/bitable/v1/apps/${FEISHU_BITABLE_TOKEN}/tables/tbl9cpBHOK7dB4BG/records`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${tenantToken}`
          },
          body: JSON.stringify({
            fields: {
              "昵称": name,
              "内容": content,
              "状态": status,
              "时间": now
            }
          })
        });
        const writeData = await writeRes.json();
        if (writeData.code !== 0) {
          console.error("Feishu write failed", writeData);
        }
      } catch (err) {
        console.error("Failed to write to Feishu", err);
      }

      // Fake success for REJECT to shadowban
      return res.status(200).json({ status: 'success' });

    } catch (e) {
      console.error(e);
      return res.status(500).json({ status: 'error', message: 'Internal Server Error' });
    }
  } 
  
  if (req.method === 'GET') {
    // 1. Get Token
    let tenantToken = '';
    try {
      const tokenRes = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_id: FEISHU_APP_ID, app_secret: FEISHU_APP_SECRET })
      });
      const tokenData = await tokenRes.json();
      tenantToken = tokenData.tenant_access_token;
    } catch (err) {
      return res.status(500).json({ status: 'error', message: 'Database auth failed' });
    }

    // 2. Read Bitable
    try {
      const readRes = await fetch(`https://open.feishu.cn/open-apis/bitable/v1/apps/${FEISHU_BITABLE_TOKEN}/tables/tbl9cpBHOK7dB4BG/records?filter=CurrentValue.[%E7%8A%B6%E6%80%81]="PASS"`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${tenantToken}`
        }
      });
      const readData = await readRes.json();
      
      let messages = [];
      if (readData.data && readData.data.items) {
        messages = readData.data.items.map(item => ({
          name: item.fields["昵称"] || '匿名',
          content: item.fields["内容"] || '',
          timestamp: item.fields["时间"] || new Date().toISOString()
        }));
      }
      return res.status(200).json(messages);
    } catch (err) {
      return res.status(500).json({ status: 'error', message: 'Failed to read data' });
    }
  }

  return res.status(405).json({ message: 'Method Not Allowed' });
}