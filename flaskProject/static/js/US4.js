document.addEventListener("DOMContentLoaded", function() {
    // 绑定表单提交事件
    document.getElementById("calculation_Form").addEventListener("submit", function(event) {
        event.preventDefault(); // 阻止表单默认提交行为
        // 获取表单数据
        const input1 = document.getElementById("input1").value;
        const input2 = document.getElementById("input2").value;
        const input3 = document.getElementById("input3").value;
        const input4 = document.getElementById("input4").value;
        // 构建请求URL
        const requestURL = `/calculate_sunscreen?input1=${input1}&input2=${input2}&input3=${input3}&input4=${input4}`;

        // 发起AJAX请求
        fetch(requestURL)
            .then(response => response.json()) // 解析JSON格式的响应
            .then(data => {
                // 更新页面上的结果
                document.getElementById("result").textContent = data.result;
            })
            .catch(error => console.error('Error:', error)); // 处理可能出现的错误
    });
});
