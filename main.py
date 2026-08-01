   from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

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
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_template = f.read()
    except Exception:
        return "Error: index.html not found. Please check file name."
    
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
                ⏳ UT Bot: Syncing...
            </div>
            <div class="tradingview-widget-container" style="margin-top: 8px; position: relative;">
                <div class="arrow-overlay" id="overlay-{item['code']}" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.85); padding: 5px 10px; border-radius: 6px; font-size: 15px; font-weight: bold; color: #8b949e; z-index: 5; border: 1px solid #8b949e;">
                    ⏳ 30s
                </div>
                <div id="tv-chart-{item['name']}" style="height: 190px; width: 100%;"></div>
                <script type="text/javascript">
                    new TradingView.widget({{
                        "width": "100%", "height": "190", "symbol": "{item['tv']}",
                        "interval": "1", "timezone": "Asia/Bangkok", "theme": "dark",
                        "style": "1", "locale": "en", "toolbar_bg": "#f1f3f6",
                        "enable_publishing": false, "hide_top_toolbar": true,
                        "hide_legend": true, "save_image": false, "container_id": "tv-chart-{item['name']}"
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
    
    symbol_codes = [s['code'] for s in SYMBOLS]
    html_content = html_template.replace("<!--CARDS_PLACEHOLDER-->", cards_html)
    html_content = html_content.replace("<!--SYMBOLS_PLACEHOLDER-->", json.dumps(symbol_codes))
    return html_content
             
