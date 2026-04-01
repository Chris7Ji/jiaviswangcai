// 留言板前端逻辑 (已对接 Vercel Serverless)
document.addEventListener('DOMContentLoaded', () => {
    loadMessages();
});

const API_BASE = 'https://jarviswangcai.vercel.app/api/messages';

function loadMessages() {
    const listEl = document.getElementById('gb-list');
    
    // 从 Vercel API 加载留言
    fetch(API_BASE)
        .then(response => response.json())
        .then(data => {
            if (!data || data.length === 0) {
                listEl.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">暂无留言，快来抢沙发吧！</div>';
                return;
            }
            
            // 倒序排列（最新的在上面）
            data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            
            let html = '';
            data.forEach(msg => {
                const name = msg.name || '匿名访客';
                const isAdmin = name.includes('钢铁侠') || name.includes('老板');
                const adminIcon = isAdmin ? '<span style="background: var(--accent-gold); color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: normal; margin-left: 5px;">站长</span>' : '';
                const cardClass = isAdmin ? 'gb-card admin' : 'gb-card';
                
                // 简单的防XSS处理
                const safeContent = msg.content.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                const safeName = name.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                
                // 格式化时间
                const timeStr = new Date(msg.timestamp).toLocaleString('zh-CN', {
                    year: 'numeric', month: '2-digit', day: '2-digit', 
                    hour: '2-digit', minute: '2-digit', hour12: false
                });
                
                html += `
                    <div class="${cardClass}">
                        <div class="gb-header">
                            <span class="gb-name">🧑‍💻 ${safeName} ${adminIcon}</span>
                            <span class="gb-time">${timeStr}</span>
                        </div>
                        <div class="gb-content">${safeContent}</div>
                    </div>
                `;
            });
            listEl.innerHTML = html;
        })
        .catch(err => {
            console.error('加载留言失败:', err);
            listEl.innerHTML = '<div style="text-align: center; color: var(--accent-blue); padding: 2rem;">系统维护中，暂时无法加载留言。</div>';
        });
}

function submitGuestbook() {
    const nameInput = document.getElementById('gb-name');
    const msgInput = document.getElementById('gb-message');
    const statusEl = document.getElementById('gb-status');
    const submitBtn = document.getElementById('gb-submit');
    
    let name = nameInput.value.trim();
    if (!name) name = "匿名访客";
    
    const content = msgInput.value.trim();
    if (!content) {
        showStatus('留言内容不能为空！', 'red');
        return;
    }
    
    if (content.length < 2) {
        showStatus('留言太短啦，多写几个字吧 (至少2个字符)', 'red');
        return;
    }

    // 界面表现为提交中
    submitBtn.disabled = true;
    submitBtn.innerText = "正在进行 DeepSeek AI 极速机审...";
    
    fetch(API_BASE, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name, content: content })
    })
    .then(res => res.json())
    .then(data => {
        msgInput.value = '';
        submitBtn.disabled = false;
        submitBtn.innerText = "提交留言";
        
        statusEl.style.display = 'block';
        statusEl.style.color = '#3D9CA8';
        statusEl.innerHTML = '✅ 留言提交成功！已通过 AI 安全初审。';
        
        loadMessages(); // 实时刷新留言列表！
        
        setTimeout(() => {
            statusEl.style.display = 'none';
        }, 5000);
    })
    .catch(err => {
        submitBtn.disabled = false;
        submitBtn.innerText = "提交留言";
        showStatus('服务器开小差了，请稍后再试', 'red');
        console.error(err);
    });
}

function showStatus(text, color) {
    const statusEl = document.getElementById('gb-status');
    statusEl.style.display = 'block';
    statusEl.style.color = color;
    statusEl.innerText = text;
}