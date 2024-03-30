document.addEventListener('DOMContentLoaded', function() {
    // 检查是否已经保存了 User ID
    chrome.storage.local.get('userid', function(result) {
        if (result.userid) {
            // 如果已经保存了 User ID，隐藏表单，显示 User ID
            document.getElementById('userid-form').style.display = 'none';
            const useridDisplay = document.createElement('p');
            useridDisplay.textContent = `大哥号: ${result.userid}`;
            useridDisplay.style.cursor = 'pointer'; // 将鼠标光标设置为指针样式
            useridDisplay.addEventListener('click', function() {
                // 点击大哥号时，隐藏显示的大哥号，重新显示输入表单
                useridDisplay.style.display = 'none';
                document.getElementById('userid-form').style.display = 'block';
            });
            document.body.appendChild(useridDisplay);
        } else {
            // 如果没有保存 User ID，显示表单
            document.getElementById('userid-form').style.display = 'block';
        }
    });

    document.getElementById('userid-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const userid = document.getElementById('userid').value;

        // 保存 User ID 到 Chrome 存储
        chrome.storage.local.set({userid: userid}, function() {
            console.log('大哥号已保存:', userid);
            // 刷新 popup 页面以显示保存的 User ID
            window.location.reload();
        });
    });
});
