// 监视页面上特定元素的出现
const timestamp = new Date().getTime(); // 获取当前时间的时间戳

function observeElementAppearance(selector, callback) {
    const observer = new MutationObserver((mutationsList, observer) => {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
            callback(elements);
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

// 当检测到错误消息时刷新页面
observeElementAppearance('[data-testid="ErrorFeedback"]', (elements) => {
    console.log('Error detected, refreshing page...');
    location.reload();
});

// 当检测到设备信息容器时提取设备信息
observeElementAppearance('[data-testid="ClusterCard_wrapper"]', (containers) => {
    const devices = [];

    containers.forEach(card => {
        const deviceName = card.querySelector('div[title]').title.trim();
        const statusSpan = card.querySelector('div.text-2xs span');
        const status = statusSpan ? statusSpan.textContent.trim() : null;
        const hardware = card.querySelector('div[data-testid="HardwareCard"] div:last-child').textContent.trim();

        devices.push({
            deviceName,
            status,
            hardware
        });
    });

    displayDeviceInfo(devices);
    postDeviceInfo(devices);
});

function displayDeviceInfo(devices) {
    const deviceInfo = devices.map(device => `机器名: ${device.deviceName}, 状态: ${device.status}, 硬件: ${device.hardware}`).join('\n');
    console.log('Device Info:', deviceInfo);
}

let userid = null;

// 从 Chrome 存储中获取 User ID
chrome.storage.local.get('userid', function (result) {
    if (result.userid) {
        userid = result.userid;
    }
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.userid) {
        userid = request.userid;
    }
});

function postDeviceInfo(devices) {
    if (!userid) {
        console.log('User ID is missing, POST request not allowed.');
        return;
    }

    fetch('https://www.你的域名.com/ionet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'User-ID': userid,
            'Timestamp': timestamp // 在请求头中添加时间戳
        },
        body: JSON.stringify(devices)
    })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => {
            console.error('Error:', error);
        });
}

// 检查当前 URL 并设置定时刷新
if (location.href === 'https://cloud.io.net/worker/devices') {
    setTimeout(() => {
        console.log('Refreshing page after 30 minutes...');
        location.reload();
    }, 30 * 60 * 1000);
}
