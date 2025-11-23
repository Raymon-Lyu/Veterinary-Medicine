async function Url2IconUrl(params) {
    const userInput = await params.quickAddApi.inputPrompt("请输入内容:", "默认值");

    try {
        const urlObj = new URL(userInput);
        const domain = urlObj.hostname;

        // 定义IconProvider接口和providers对象
        // src: https://github.com/joethei/obsidian-link-favicon/blob/master/src/provider.ts
        const providers = {
            'google': {name: 'Google', url: domain => Promise.resolve("https://www.google.com/s2/favicons?domain=" + domain)},
            'duckduckgo': {
                name: 'DuckDuckGo',
                url: domain => Promise.resolve("https://icons.duckduckgo.com/ip3/" + domain + ".ico")
            },
            'iconhorse': {name: 'Icon Horse', url: domain => Promise.resolve("https://icon.horse/icon/" + domain)},
            'splitbee': {name: 'Splitbee', url: domain => Promise.resolve("https://favicon.splitbee.io/?url=" + domain)}
        };

        // 选择供应商
        const selectedProvider = 'splitbee'; // 这里可以根据需求更改

        // 获取图标URL
        const iconUrl = await providers[selectedProvider].url(domain);

        new Notice(iconUrl, 5000); // 显示通知

        // 组合成Markdown格式的超链接图片
        const markdownLink = `[![](${iconUrl})](${userInput})`;

        return markdownLink;
    } catch (error) {
        new Notice("输入的内容不是有效的URL，请重新输入。", 5000);
        return null;
    }
}

module.exports = Url2IconUrl;