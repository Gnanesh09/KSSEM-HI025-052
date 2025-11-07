TRANSLATIONS = {
    'en': {
        'title': '🌾 GreenChain',
        'subtitle': 'Blockchain-Powered Crop Insurance',
        'dashboard': {
            'welcome': 'Welcome',
            'my_fields': 'My Fields',
            'approved': 'Approved Claims',
            'payout': 'Total Payouts',
        },
        'claim': {
            'title': 'File Insurance Claim',
            'drought': 'Drought ☀️',
            'flood': 'Flood 🌊',
            'pest': 'Pest Attack 🐛',
            'hailstorm': 'Hailstorm 🌧️',
            'approved': '✅ CLAIM APPROVED!',
            'rejected': '❌ CLAIM REJECTED',
            'payout': 'Payout Amount',
        },
        'satellite': {
            'title': 'Satellite Verification',
            'healthy': 'Healthy ✅',
            'stressed': 'Stressed ⚠️',
            'damaged': 'Damaged ❌',
        },
        'prices': {
            'title': 'Check Fair Prices',
            'fair': 'Fair Market Price',
            'offered': 'Typically Offered',
        },
        'blockchain': {
            'title': 'Blockchain Explorer',
            'blocks': 'Total Blocks',
            'transactions': 'Total Transactions',
        },
    },
    'hi': {
        'title': '🌾 ग्रीनचेन',
        'dashboard': {'welcome': 'स्वागत है', 'my_fields': 'मेरे खेत', 'approved': 'स्वीकृत दावे', 'payout': 'कुल भुगतान'},
        'claim': {'title': 'बीमा दावा दाखिल करें', 'approved': '✅ दावा स्वीकृत!', 'rejected': '❌ दावा अस्वीकृत'},
    },
    'kn': {
        'title': '🌾 ಗ್ರೀನ್‌ಚೈನ್',
        'dashboard': {'welcome': 'ಸ್ವಾಗತ', 'my_fields': 'ನನ್ನ ಭೂಮಿಗಳು', 'approved': 'ಅನುಮೋದಿತ ದಾವೆಗಳು', 'payout': 'ಒಟ್ಟು ಪಾವತಿಗಳು'},
        'claim': {'title': 'ವಿಮೆ ದಾವೆ ಸಲ್ಲಿಸಿ', 'approved': '✅ ದಾವೆ ಅನುಮೋದಿತ!', 'rejected': '❌ ದಾವೆ ಅಸ್ವೀಕೃತ'},
    },
    'te': {
        'title': '🌾 గ్రీన్‌చెయిన్',
        'dashboard': {'welcome': 'స్వాగతం', 'my_fields': 'నా భూములు', 'approved': 'ఆమోదిత దావాలు', 'payout': 'మొత్తం చెల్లింపులు'},
        'claim': {'title': 'బీమా దావా సమర్పించండి', 'approved': '✅ దావా ఆమోదించబడింది!', 'rejected': '❌ దావా తిరస్కరించబడింది'},
    },
}

def get_text(lang: str, key: str, default: str = None) -> str:
    keys = key.split('.')
    value = TRANSLATIONS.get(lang, {})
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, {})
        else:
            return default or key
    
    return value or default or key
