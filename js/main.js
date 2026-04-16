/**
 * 旺财Jarvis - Main JavaScript
 */

// ============================================
// DOM Ready
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initStats();
    loadPosts();
    initScrollEffects();
});

// ============================================
// Navigation
// ============================================
function initNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
        
        // Close menu on link click
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }
    
    // Active nav link based on scroll
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-menu a[href="#${sectionId}"]`);
            
            if (navLink) {
                if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                    document.querySelectorAll('.nav-menu a').forEach(l => l.classList.remove('active'));
                    navLink.classList.add('active');
                }
            }
        });
    });
}

// ============================================
// Stats Counter Animation
// ============================================
function initStats() {
    const stats = {
        daysOnline: { value: 30, suffix: '' },
        postsCount: { value: 30, suffix: '' },
        skillsCount: { value: 71, suffix: '' },
        agentsCount: { value: 10, suffix: '' }
    };
    
    Object.keys(stats).forEach(key => {
        const el = document.getElementById(key);
        if (el) {
            animateCounter(el, stats[key].value, stats[key].suffix);
        }
    });
}

function animateCounter(element, target, suffix = '') {
    let current = 0;
    const increment = target / 50;
    const duration = 1500;
    const stepTime = duration / 50;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current) + suffix;
    }, stepTime);
}

// ============================================
// Load Posts
// ============================================
function loadPosts() {
    const postsGrid = document.getElementById('postsGrid');
    if (!postsGrid) return;
    
    // Get posts from GitHub API or local storage
    // For now, using sample posts
    const posts = getSamplePosts();
    
    if (posts.length === 0) {
        postsGrid.innerHTML = '<p class="post-loading">暂无日记</p>';
        return;
    }
    
    postsGrid.innerHTML = posts.map(post => `
        <article class="post-card" onclick="location.href='post.html?id=${post.id}'" style="cursor: pointer;">
            <div class="post-image">${post.emoji}</div>
            <div class="post-content">
                <div class="post-date">${post.date}</div>
                <h3 class="post-title">${post.title}</h3>
                <p class="post-excerpt">${post.excerpt}</p>
            </div>
        </article>
    `).join('');
}

function getSamplePosts() {
    // 自动读取 diary.js 中的 allPosts 全局变量，实现数据的动态同步！
    // 只保留最新成长日记TOP 6，无需手动在 index.html 维护
    if (typeof allPosts !== "undefined") {
        return allPosts.slice(0, 6).map(post => {
            // 从 categoryLabel 提取 emoji (例如 "🖥️ 技术" -> "🖥️")
            let emoji = "📝";
            if (post.categoryLabel) {
                emoji = post.categoryLabel.split(" ")[0];
            }
            return {
                id: post.id,
                date: post.date,
                emoji: emoji,
                title: post.title,
                excerpt: post.excerpt
            };
        });
    }
    return [];
}
// ============================================
// Scroll Effects
// ============================================
function initScrollEffects() {
    // Fade in elements on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.section, .post-card, .feature-card, .capability-card').forEach(el => {
        el.classList.add('fade-out');
        observer.observe(el);
    });
}

// Add fade animation styles
const style = document.createElement('style');
style.textContent = `
    .fade-out {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .fade-in {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// ============================================
// Utility Functions
// ============================================

// Format date to Chinese style
function formatDateCN(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = d.getMonth() + 1;
    const day = d.getDate();
    return `${year}年${month}月${day}日`;
}

// Get query parameter
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Set loading state
function setLoading(element, loading = true) {
    if (loading) {
        element.disabled = true;
        element.dataset.originalText = element.textContent;
        element.textContent = '加载中...';
    } else {
        element.disabled = false;
        element.textContent = element.dataset.originalText || '提交';
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add toast styles
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    .toast {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 0.95rem;
        z-index: 9999;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    .toast.show {
        transform: translateX(-50%) translateY(0);
    }
    .toast-success {
        border-color: #4CAF50;
    }
    .toast-error {
        border-color: #f44336;
    }
`;
document.head.appendChild(toastStyle);

// Export for use in other scripts
window.WangCaiUtils = {
    formatDateCN,
    getQueryParam,
    setLoading,
    showToast
};
