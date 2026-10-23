import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Super Mario Game", page_icon="🍄", layout="centered"
)

st.title("🍄 Super Mario Bros - Streamlit Edition")
st.write(
    "🎮 **Hướng dẫn điều khiển:** Dùng phím **A/D** hoặc **Mũi tên Trái/Phải**"
    " để di chuyển, **Space** hoặc **W/Mũi tên Lên** để nhảy!"
)

# Mã HTML/JS chứa game Mario mượt 60 FPS
mario_html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #111; display: flex; justify-content: center; align-items: center; height: 100vh; }
        canvas { border: 3px solid #fff; background: #5c94fc; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="350"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Nhân vật Mario
        let mario = {
            x: 50, y: 200, width: 24, height: 32,
            dx: 0, dy: 0, speed: 4, gravity: 0.4,
            jumpPower: -9.5, grounded: false
        };

        let keys = {};
        let coins = 0;
        let coinObj = { x: 300, y: 180, size: 12, collected: false };

        document.addEventListener("keydown", (e) => keys[e.code] = true);
        document.addEventListener("keyup", (e) => keys[e.code] = false);

        function update() {
            // Di chuyển
            if (keys["ArrowRight"] || keys["KeyD"]) mario.x += mario.speed;
            if (keys["ArrowLeft"] || keys["KeyA"]) mario.x -= mario.speed;

            // Nhảy
            if ((keys["Space"] || keys["ArrowUp"] || keys["KeyW"]) && mario.grounded) {
                mario.dy = mario.jumpPower;
                mario.grounded = false;
            }

            // Trọng lực & vị trí
            mario.dy += mario.gravity;
            mario.y += mario.dy;

            // Giới hạn màn hình
            if (mario.x < 0) mario.x = 0;
            if (mario.x + mario.width > canvas.width) mario.x = canvas.width - mario.width;

            // Chạm đất (Mặt đất ở y = 280)
            if (mario.y + mario.height >= 280) {
                mario.y = 280 - mario.height;
                mario.dy = 0;
                mario.grounded = true;
            }

            // Ăn đồng xu
            if (!coinObj.collected && 
                mario.x < coinObj.x + coinObj.size &&
                mario.x + mario.width > coinObj.x &&
                mario.y < coinObj.y + coinObj.size &&
                mario.y + mario.height > coinObj.y) {
                coinObj.collected = true;
                coins += 1;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Mặt đất & Đồi núi
            ctx.fillStyle = "#e07438";
            ctx.fillRect(0, 280, canvas.width, 70);
            ctx.fillStyle = "#48a048";
            ctx.fillRect(0, 280, canvas.width, 10);

            // Vẽ Đồng xu
            if (!coinObj.collected) {
                ctx.fillStyle = "#ffd700";
                ctx.beginPath();
                ctx.arc(coinObj.x, coinObj.y, coinObj.size/2, 0, Math.PI * 2);
                ctx.fill();
            }

            // Vẽ Mario
            ctx.fillStyle = "#d82800"; // Áo đỏ
            ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            ctx.fillStyle = "#002490"; // Quần xanh
            ctx.fillRect(mario.x, mario.y + 16, mario.width, 16);

            // Hiển thị điểm
            ctx.fillStyle = "#fff";
            ctx.font = "16px Arial";
            ctx.fillText("💰 Đồng xu: " + coins, 15, 30);
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

# Nhúng vào Streamlit
components.html(mario_html_code, height=380)
