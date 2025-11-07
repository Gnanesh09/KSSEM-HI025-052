// lib/translations.ts
export interface Translations {
  [key: string]: {
    [key: string]: any
  }
}

export const translations: Translations = {
  en: {
    nav: {
      home: "Home",
      dashboard: "Dashboard",
      fileClaim: "File Claim",
      satellite: "Satellite",
      prices: "Prices",
      blockchain: "Blockchain",
      logout: "Logout",
    },
    home: {
      title: "🌾 GreenChain",
      subtitle: "Blockchain-Powered Crop Insurance",
      tagline: "Instant verification. Zero fraud. Fair payouts.",
      features: {
        satellite: "Satellite Truth",
        blockchain: "Blockchain Security",
        pricing: "Fair Pricing",
      },
      cta: "Start Demo",
    },
    dashboard: {
      welcome: "Welcome",
      myFields: "My Fields",
      claimsApproved: "Claims Approved",
      totalPayouts: "Total Payouts",
      viewDetails: "View Details",
    },
    fileClaim: {
      title: "File Insurance Claim",
      selectField: "Select Field",
      damageType: "Type of Damage",
      drought: "Drought",
      flood: "Flood",
      pest: "Pest Attack",
      hailstorm: "Hailstorm",
      submit: "Submit Claim",
      approvalMessage: "✅ Claim APPROVED!",
      rejectionMessage: "❌ Claim REJECTED",
      payout: "Payout Amount",
    },
    satellite: {
      title: "Satellite Verification",
      before: "Before",
      after: "After",
      ndvi: "NDVI Score",
      healthy: "Healthy",
      stressed: "Stressed",
      damaged: "Damaged",
    },
    prices: {
      title: "Check Fair Prices",
      commodity: "Select Commodity",
      market: "Select Market",
      checkPrice: "Check Price",
      fairPrice: "Fair Price",
      offeredPrice: "Offered Price",
    },
    blockchain: {
      title: "Blockchain Explorer",
      totalBlocks: "Total Blocks",
      totalTransactions: "Total Transactions",
      blockHash: "Block Hash",
      viewBlock: "View Block",
    },
  },
  hi: {
    nav: {
      home: "होम",
      dashboard: "डैशबोर्ड",
      fileClaim: "दावा दाखिल करें",
      satellite: "उपग्रह",
      prices: "कीमतें",
      blockchain: "ब्लॉकचेन",
      logout: "लॉग आउट",
    },
    home: {
      title: "🌾 ग्रीनचेन",
      subtitle: "ब्लॉकचेन-संचालित फसल बीमा",
      tagline: "तत्काल सत्यापन। कोई欺 नहीं। न्यायसंगत भुगतान।",
      features: {
        satellite: "उपग्रह सत्य",
        blockchain: "ब्लॉकचेन सुरक्षा",
        pricing: "न्यायसंगत मूल्य",
      },
      cta: "डेमो शुरू करें",
    },
    fileClaim: {
      title: "बीमा दावा दाखिल करें",
      selectField: "खेत चुनें",
      damageType: "नुकसान का प्रकार",
      drought: "सूखा",
      flood: "बाढ़",
      pest: "कीट का हमला",
      hailstorm: "ओलावृष्टि",
      submit: "दावा जमा करें",
      approvalMessage: "✅ दावा स्वीकृत!",
      rejectionMessage: "❌ दावा अस्वीकृत",
      payout: "भुगतान राशि",
    },
  },
  kn: {
    nav: {
      home: "ಹೋಮ್",
      dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
      fileClaim: "ದಾವೆ ಸಲ್ಲಿಸಿ",
      satellite: "ಉಪಗ್ರಹ",
      prices: "ಬೆಲೆಗಳು",
      blockchain: "ಬ್ಲಾಕ್‌ಚೈನ್",
      logout: "ಲಾಗ್ ಔಟ್",
    },
    home: {
      title: "🌾 ಗ್ರೀನ್‌ಚೈನ್",
      subtitle: "ಬ್ಲಾಕ್‌ಚೈನ್-ಚಾಲಿತ ಬೆಳೆ ವಿಮೆ",
      tagline: "ತತ್ಕ್ಷಣ ಪರಿಶೀಲನೆ। ವಂಚನೆ ಇಲ್ಲ। ನ್ಯಾಯಯುತ ಪಾವತಿಗಳು।",
      features: {
        satellite: "ಉಪಗ್ರಹ ಸತ್ಯ",
        blockchain: "ಬ್ಲಾಕ್‌ಚೈನ್ ಸುರಕ್ಷೆ",
        pricing: "ನ್ಯಾಯಯುತ ಬೆಲೆ",
      },
      cta: "ಡೆಮೋ ಪ್ರಾರಂಭಿಸಿ",
    },
  },
  te: {
    nav: {
      home: "హోమ్",
      dashboard: "డ్యాష్‌బోర్డ్",
      fileClaim: "దావా సమర్పించండి",
      satellite: "ఉపగ్రహం",
      prices: "ధరలు",
      blockchain: "బ్లాక్‌చెయిన్",
      logout: "లాగ్ అవుట్",
    },
    home: {
      title: "🌾 గ్రీన్‌చెయిన్",
      subtitle: "బ్లాక్‌చెయిన్-ఆధారిత పంట బీమా",
      tagline: "తక్షణ ధృవీకరణ. కోటి వంచన లేదు. న్యాయమైన చెల్లింపులు.",
      features: {
        satellite: "ఉపగ్రహ సత్యం",
        blockchain: "బ్లాక్‌చెయిన్ సురక్ష",
        pricing: "న్యాయమైన ధర",
      },
      cta: "డెమోను ప్రారంభించండి",
    },
  },
}
