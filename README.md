
---

## 🚀 Quickstart (Local Run)

1. **Clone the repo and enter backend directory**

    ```
    git clone https://github.com/yourusername/GreenChain.git
    cd GreenChain/backend
    python -m venv venv
    venv\Scripts\activate
    ```

2. **Install backend dependencies and run FastAPI**

    ```
    pip install -r requirements.txt
    uvicorn app.main:app --reload    # Listen on http://localhost:8000
    ```

3. **Open a new terminal for the frontend**

    ```
    cd GreenChain/backend/frontend
    venv\Scripts\activate
    pip install -r requirements.txt
    streamlit run app.py             # Open http://localhost:8501
    ```

---

## 🧭 How to Use (Farmer Journey)

1. **Register as Farmer**: Enter name, phone, village (Dashboard tab)
2. **Add Your Field**: Crop, size, location, GPS (in Dashboard)
3. **File Crop Insurance Claim**: Select field, type of damage (e.g. drought), NDVI auto-checks satellite data for approval
4. **See Approval**: If NDVI/crop loss > threshold, get instant approval. Transparent blockchain record for every claim
5. **Get Paid**: Choose UPI, card, or bank transfer. Scan QR for instant payout to your bank.
6. **Build Credit & Get Loans**: Track your credit score as you build good claim history. Instantly see bank loan offers matched to your profile.
7. **Monitor, Learn, and Connect**: Real-time weather/price info, track NDVI/field health, learn from guides and community.

---

## 📶 Demo/Test Data

- Uses SQLite DB and in-memory blockchain (no real money moves in demo mode)
- All UPI/card payments use Razorpay test keys or offline QR
- Satellite & weather data is mocked for hackathon, production-ready for real APIs

---

## 📊 Sample Analytics

- Total farmers, claims, payouts, field areas (dashboard)
- Approval rate, avg payout, damage by crop/region
- Transaction records on blockchain explorer

---

## 🌈 Main Technologies Used

- **Backend**: FastAPI, SQLAlchemy, SQLite, custom blockchain Python module, Razorpay SDK, qrcode
- **Frontend**: Streamlit, Plotly, Pandas, Requests
- **Other**: Twilio (SMS), OpenCV/TensorFlow (optionally for AI), Pydantic, multilingual support

---

## 💡 Extending for Production

- Replace with mainnet blockchain (Polygon, Ethereum, Solana)
- Plug in real NDVI + Copernicus/Sentinel API for live satellite data
- Integrate open banking APIs for automatic lending/repayment
- Use actual UPI merchant account and KYC
- Deploy on cloud, containerize with Docker

---

## 🛠 Troubleshooting

| Issue                       | Solution                                 |
|-----------------------------|------------------------------------------|
| Streamlit “Running...”      | Check backend is up and reachable        |
| 500 Internal Server Error   | Check backend for Python errors, restart |
| Database errors             | Delete greenchain.db, backend re-creates |
| UPI QR not showing          | Restart backend, ensure qrcode lib works |
| Stuck claim approval        | Check NDVI thresholds and satellite code |

---

## 🤝 Contributing

Pull requests and issue reports are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

MIT License. See [LICENSE](LICENSE).

---

## 👨‍💻 Credits

Built by [Your Name/Team] for [Your Hackathon/Event] — made with ❤️ for Indian farmers!

---

## 📚 Documentation & API

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Full user guide (in the Streamlit app, Home or Quick Start tab)

---

## 🚨 Disclaimer

This is a demo/hackathon codebase. DO NOT use with real funds or farm data until it has passed security, privacy, and regulatory audits.

---

## 📮 Contact

Open issues or reach out at [your-email@example.com] if you want to use, extend, or help deploy GreenChain!

