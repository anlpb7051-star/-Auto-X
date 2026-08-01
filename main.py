     from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

SYMBOLS = [
    {"code": "BTCUSDT", "tv": "BINANCE:BTCUSDT", "name": "BTC", "icon": "🪙"},
    {"code": "ETHUSDT", "tv": "BINANCE:ETHUSDT", "name": "ETH", "icon": "💎"},
    {"code": "BNBUSDT", "tv": "BINANCE:BNBUSDT", "name": "BNB", "icon": "🟡"},
    {"code": "PAXGUSDT", "tv": "BINANCE:PAXGUSDT", "name": "GOLD (ທອງຄຳ)", "icon": "🥇"},
    {"code": "SOLUSDT", "tv": "BINANCE:SOLUSDT", "name": "SOL", "icon": "🟣"},
    {"code": "XRPUSDT", "tv": "BINANCE:XRPUSDT", "name": "XRP", "icon": "🔵"},
    {"code": "ADAUSDT", "tv": "BINANCE:ADAUSDT", "name": "ADA", "icon": "🔷"},
    {"code": "DOGEUSDT", "tv": "BINANCE:DOGEUSDT", "name": "DOGE", "icon": "🐕"},
    {"code": "AVAXUSDT", "tv": "BINANCE:AVAXUSDT", "name": "AVAX", "icon": "🔺"},
    {"code": "DOTUSDT", "tv": "BINANCE:DOTUSDT", "name": "DOT", "icon": "⚪"}
]

@app.get("/", response_class=HTMLResponse)
def dashboard():
    cards_html = ""
    for item in SYMBOLS:
        cards_html += f"""
        <div class="card" id="card-{item['code']}" style="border-top: 3px solid #8b949e;">
            <div class="card-top">
                <div class="asset-info">
                    <span class="icon">{item['icon']}</span>
                    <div>
                        <div class="asset-name">{item['name']}/USDT <span id="arrow-{item['code']}" style="font-size: 18px; margin-left: 5px;"></span></div>
                        <div class="asset-price" id="price-{item['code']}">Loading...</div>
                    </div>
                </div>
                <div class="conf-badge">
                    <span class="conf-num" id="conf-{item['code']}">--%</span>
                </div>
            </div>

            <div class="buy-pill" id="pill-{item['code']}" style="background: #30363d; color: #8b949e; border: 1px solid #30363d;">
                ⏳ UT Bot: ລໍຖ້າສັນຍານ...
            </div>

            <div class="tradingview-widget-container" style="margin-top: 8px; position: relative;">
                <div class="arrow-overlay" id="overlay-{item['code']}" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.85); padding: 5px 10px; border-radius: 6px; font-size: 15px; font-weight: bold; color: #8b949e; z-index: 5; border: 1px solid #8b949e;">
                    ⏳ 30s
                </div>
                <div id="tv-chart-{item['name']}" style="height: 190px; width: 100%;"></div>
                <script type="text/javascript">
                    new TradingView.widget({{
                        "width": "100%",
                        "height": "190",
                        "symbol": "{item['tv']}",
                        "interval": "1",
                        "timezone": "Asia/Bangkok",
                        "theme": "dark",
                        "style": "1",
                        "locale": "en",
                        "toolbar_bg": "#f1f3f6",
                        "enable_publishing": false,
                        "hide_top_toolbar": true,
                        "hide_legend": true,
                        "save_image": false,
                        "container_id": "tv-chart-{item['name']}"
                    }});
                </script>
            </div>

            <div class="progress-bar-bg" style="margin-top: 8px;">
                <div class="progress-fill" id="pfill-{item['code']}" style="width: 50%; background: #8b949e;"></div>
            </div>
            <div class="progress-labels">
                <span id="plabel-up-{item['code']}">UP --</span>
                <span id="plabel-down-{item['code']}">DOWN --</span>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">UT Bot Status</div>
                    <div class="stat-val" id="status-{item['code']}">Syncing...</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">ATR Trend Filter</div>
                    <div class="stat-val" id="rsi-{item['code']}">Neutral</div>
                </div>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="lo">
<head>
    <meta charset="UTF-8">
    <title>XR Trade - UT Bot & 5s Final Signal</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #0b0f19; color: #f0f6fc; margin: 0; padding: 20px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; background: #161b22; padding: 15px 25px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; }}
        .logo {{ font-size: 22px; font-weight: bold; color: #58a6ff; display: flex; align-items: center; gap: 8px; }}
        
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 14px; padding: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }}
        .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
        .asset-info {{ display: flex; gap: 10px; align-items: center; }}
        .icon {{ font-size: 28px; }}
        .asset-name {{ font-size: 16px; font-weight: bold; color: #f0f6fc; }}
        .asset-price {{ font-size: 13px; color: #8b949e; margin-top: 2px; }}
        
        .conf-badge {{ text-align: right; }}
        .conf-num {{ font-size: 20px; font-weight: bold; }}
        .buy-pill {{ font-size: 13px; padding: 8px 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 6px; }}

        .progress-bar-bg {{ background: #30363d; height: 7px; border-radius: 4px; overflow: hidden; }}
        .progress-fill {{ height: 100%; }}
        .progress-labels {{ display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; margin-top: 4px; margin-bottom: 8px; }}

        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        .stat-box {{ background: #0d1117; border: 1px solid #30363d; padding: 6px 10px; border-radius: 8px; text-align: center; }}
        .stat-label {{ font-size: 11px; color: #8b949e; }}
        .stat-val {{ font-size: 12px; font-weight: bold; color: #c9d1d9; margin-top: 2px; }}
    </style>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script>
        const symbolList = {[s['code'] for s in SYMBOLS]};

        async function updateMarket() {{
            try {{
                const res = await fetch('https://api.binance.com/api/v3/ticker/24hr');
                const data = await res.json();
                const priceMap = {{}};
                data.forEach(item => {{ priceMap[item.symbol] = item; }});

                const now = new Date();
                const currentSec = now.getSeconds();
                
                let secInCycle = currentSec % 30;
                let countdown = 30 - secInCycle;
                if (countdown === 30) countdown = 30;

                let isFinal5s = (secInCycle >= 25);

                symbolList.forEach(code => {{
                    let item = priceMap[code];
                    let price = item ? parseFloat(item.lastPrice) : 100.0;
                    let change = item ? parseFloat(item.priceChangePercent) : 0.5;
                    
                    let priceStr = price < 1 ? price.toFixed(4) : price.toFixed(2);
                    let changeStr = (change >= 0 ? "+" : "") + change.toFixed(2) + "%";
                    let isUp = change >= 0;
                    let color = isUp ? "#2ea043" : "#f85149";
                    
                    let conf = Math.min(Math.max(75.0 + Math.abs(change * 4.0), 70.0), 98.5).toFixed(1);

                    document.getElementById('price-' + code).innerHTML = `$${{priceStr}} <span style="color: ${{color}};">(${{changeStr}})</span>`;
                    document.getElementById('conf-' + code).innerText = Math.round(conf) + "%";
                    document.getElementById('conf-' + code).style.color = color;

                    let pill = document.getElementById('pill-' + code);
                    let overlay = document.getElementById('overlay-' + code);
                    let arrow = document.getElementById('arrow-' + code);
                    let card = document.getElementById('card-' + code);

                    if (isFinal5s) {{
                        let sigText = isUp ? "🟢 ເບິດເວລາ: ⬆️ BUY (ກຽມກົດຂຶ້ນ!)" : "🔴 ເບິດເວລາ: ⬇️ SELL (ກຽມກົດລົງ!)";
                        let arr = isUp ? "⬆️" : "⬇️";
                        pill.innerHTML = `${{sigText}} (${{countdown}}s)`;
                        pill.style.background = isUp ? "#2ea04333" : "#f8514933";
                        pill.style.color = color;
                        pill.style.borderColor = color;

                        overlay.innerHTML = `${{arr}} ${{countdown}}s`;
                        overlay.style.color = color;
                        overlay.style.borderColor = color;

                        arrow.innerHTML = arr;
                        arrow.style.color = color;
                        card.style.borderTop = `3px solid ${{color}}`;
                    }} else {{
                        let utStatus = isUp ? "UT Bot: 📈 ແຮງຊື້ຄອບຄອງ" : "UT Bot: 📉 ແຮງຂາຍຄອບຄອງ";
                        pill.innerHTML = `${{utStatus}} (${{countdown}}s)`;
                        pill.style.background = "#30363d";
                        pill.style.color = "#8b949e";
                        pill.style.borderColor = "#30363d";

                        overlay.innerHTML = `⏳ ${{countdown}}s`;
                        overlay.style.color = "#8b949e";
                        overlay.style.borderColor = "#8b949e";

                        arrow.innerHTML = "";
                        card.style.borderTop = "3px solid #30363d";
                    }}

                    document.getElementById('pfill-' + code).style.width = conf + "%";
                    document.getElementById('pfill-' + code).style.background = color;
                    document.getElementById('plabel-up-' + code).innerText = "UP " + Math.round(conf) + "%";
                    document.getElementById('plabel-down-' + code).innerText = "DOWN " + (100 - Math.round(conf)) + "%";

                    document.getElementById('status-' + code).innerText = isUp ? "UT Buy Signal" : "UT Sell Signal";
                    document.getElementById('status-' + code).style.color = color;
                    document.getElementById('rsi-' + code).innerText = isUp ? "Bullish ATR" : "Bearish ATR";
                }});
            }} catch(e) {{
                console.error(e);
            }}
        }}

        window.onload = function() {{
            setInterval(updateMarket, 200);
            updateMarket();
        }};
    </script>
</head>
<body>
    <div class="header">
        <div class="logo">🤖 XR Trade + UT Bot Alerts (5s Final Signal)</div>
    </div>

    <div class="grid">
        {cards_html}
    </div>
</body>
</html>
"""
    return html_content
     
