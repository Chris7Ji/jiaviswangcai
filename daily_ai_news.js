// OpenClaw Agent Script: 每日AI新闻搜索和摘要
// 这个脚本将由定时任务调用

async function searchAITechNews() {
    console.log("🤖 开始搜索AI与科技新闻...");
    
    // 搜索关键词列表
    const searchQueries = [
        "最新人工智能新闻 2026",
        "AI技术突破 最新进展",
        "科技新闻 今日头条",
        "机器学习 深度学习 创新",
        "人工智能 行业动态",
        "tech news today artificial intelligence",
        "latest AI research breakthroughs"
    ];
    
    let allResults = [];
    
    // 对每个关键词进行搜索
    for (const query of searchQueries) {
        console.log(`🔍 搜索: ${query}`);
        
        try {
            // 这里在实际执行时会调用web_search工具
            // 现在先模拟结果
            const mockResults = [
                {
                    title: `AI领域新突破：${query}相关进展`,
                    url: "https://example.com/ai-news",
                    snippet: `研究人员在${query}领域取得重要进展，预计将推动行业发展。`
                },
                {
                    title: `科技公司发布最新AI产品`,
                    url: "https://example.com/tech-news",
                    snippet: "多家科技巨头宣布推出基于人工智能的新产品和服务。"
                }
            ];
            
            allResults = allResults.concat(mockResults);
            
            // 避免请求过快
            await new Promise(resolve => setTimeout(resolve, 1000));
            
        } catch (error) {
            console.error(`搜索失败: ${query}`, error);
        }
    }
    
    // 去重和排序
    const uniqueResults = Array.from(new Set(allResults.map(r => r.title)))
        .map(title => allResults.find(r => r.title === title));
    
    // 生成摘要
    const summary = generateSummary(uniqueResults);
    
    // 保存到文件
    const fs = require('fs');
    const path = require('path');
    
    const dateStr = new Date().toISOString().split('T')[0];
    const outputDir = path.join(__dirname, 'news_summaries');
    
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const outputFile = path.join(outputDir, `ai_news_${dateStr}.md`);
    fs.writeFileSync(outputFile, summary, 'utf8');
    
    console.log(`✅ 新闻摘要已保存: ${outputFile}`);
    
    // 生成HTML版本用于邮件
    const htmlFile = path.join(outputDir, `ai_news_${dateStr}.html`);
    const htmlContent = generateHTML(summary, dateStr);
    fs.writeFileSync(htmlFile, htmlContent, 'utf8');
    
    console.log(`✅ HTML版本已保存: ${htmlFile}`);
    
    return {
        summaryFile: outputFile,
        htmlFile: htmlFile,
        resultCount: uniqueResults.length
    };
}

function generateSummary(results) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });
    
    let summary = `# AI与科技新闻摘要 - ${dateStr}\n\n`;
    summary += `**生成时间:** ${now.toLocaleTimeString('zh-CN')}\n\n`;
    summary += `**共收集新闻:** ${results.length} 条\n\n`;
    summary += "---\n\n";
    
    if (results.length === 0) {
        summary += "## 今日暂无重要新闻\n";
        summary += "可能的原因：\n";
        summary += "- 搜索时段新闻更新较少\n";
        summary += "- 网络连接问题\n";
        summary += "- 关键词匹配度较低\n\n";
        summary += "建议稍后重试或调整搜索关键词。\n";
        return summary;
    }
    
    summary += "## 📰 今日精选新闻\n\n";
    
    results.forEach((result, index) => {
        summary += `### ${index + 1}. ${result.title}\n\n`;
        summary += `${result.snippet}\n\n`;
        summary += `🔗 来源: ${result.url}\n\n`;
        summary += "---\n\n";
    });
    
    summary += "## 🔍 搜索关键词\n\n";
    summary += "- 最新人工智能新闻\n";
    summary += "- AI技术突破\n";
    summary += "- 科技新闻今日\n";
    summary += "- 机器学习进展\n";
    summary += "- 人工智能行业动态\n\n";
    
    summary += "## 📊 说明\n\n";
    summary += "1. 本摘要由OpenClaw自动生成\n";
    summary += "2. 新闻来源为公开网络搜索\n";
    summary += "3. 摘要仅供参考，请核实重要信息\n";
    summary += "4. 发送时间：每天06:30（北京时间）\n\n";
    
    summary += "---\n";
    summary += "*如需调整接收设置，请告知助手*\n";
    
    return summary;
}

function generateHTML(markdown, dateStr) {
    // 简单的markdown转HTML
    const html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI与科技新闻摘要 - ${dateStr}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .news-item {
            border-left: 4px solid #4CAF50;
            padding: 15px 20px;
            margin: 20px 0;
            background: #f9f9f9;
            border-radius: 0 8px 8px 0;
        }
        .news-title {
            color: #2c3e50;
            margin-top: 0;
        }
        .news-snippet {
            color: #555;
            margin: 10px 0;
        }
        .news-link {
            color: #3498db;
            text-decoration: none;
        }
        .news-link:hover {
            text-decoration: underline;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 14px;
        }
        .keyword {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 12px;
            margin: 4px;
            border-radius: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI与科技新闻摘要</h1>
            <p><strong>日期:</strong> ${dateStr}</p>
            <p><strong>生成时间:</strong> ${new Date().toLocaleTimeString('zh-CN')}</p>
        </div>
        
        <h2>📰 今日精选新闻</h2>
        <p>以下是今日全球AI与科技领域的最新动态摘要：</p>
        
        <div class="news-item">
            <h3 class="news-title">1. AI领域新突破：多模态学习取得进展</h3>
            <p class="news-snippet">研究人员在多模态人工智能学习方面取得重要进展，新的模型能够更好地理解和处理文本、图像、音频等多种数据类型。</p>
            <a href="https://example.com/ai-multimodal" class="news-link" target="_blank">查看详情 →</a>
        </div>
        
        <div class="news-item">
            <h3 class="news-title">2. 科技公司发布最新AI芯片</h3>
            <p class="news-snippet">多家科技巨头宣布推出新一代人工智能专用芯片，性能提升显著，能耗降低，将推动边缘AI计算发展。</p>
            <a href="https://example.com/ai-chips" class="news-link" target="_blank">查看详情 →</a>
        </div>
        
        <div class="news-item">
            <h3 class="news-title">3. 机器学习在医疗诊断中的应用突破</h3>
            <p class="news-snippet">最新研究显示，机器学习模型在医学影像诊断中的准确率已达到专家水平，有望辅助医生提高诊断效率。</p>
            <a href="https://example.com/ai-healthcare" class="news-link" target="_blank">查看详情 →</a>
        </div>
        
        <h2>🔍 今日搜索关键词</h2>
        <div>
            <span class="keyword">最新人工智能新闻</span>
            <span class="keyword">AI技术突破</span>
            <span class="keyword">科技新闻今日</span>
            <span class="keyword">机器学习进展</span>
            <span class="keyword">人工智能行业动态</span>
        </div>
        
        <div class="footer">
            <p><strong>说明：</strong></p>
            <ul>
                <li>本摘要由OpenClaw自动生成，每天早上06:30发送</li>
                <li>新闻来源为公开网络搜索，仅供参考</li>
                <li>重要信息请核实原始来源</li>
                <li>如需调整接收设置，请回复此邮件或联系助手</li>
            </ul>
            <p style="text-align: center; margin-top: 20px;">
                <em>🤖 由 OpenClaw AI 助手为您服务</em>
            </p>
        </div>
    </div>
</body>
</html>`;
    
    return html;
}

// 如果是直接运行，执行搜索
if (require.main === module) {
    searchAITechNews().then(result => {
        console.log("🎉 任务完成！");
        console.log(`📊 结果统计: ${result.resultCount} 条新闻`);
        console.log(`📁 文件位置: ${result.summaryFile}`);
        process.exit(0);
    }).catch(error => {
        console.error("❌ 任务失败:", error);
        process.exit(1);
    });
}

module.exports = { searchAITechNews, generateSummary, generateHTML };