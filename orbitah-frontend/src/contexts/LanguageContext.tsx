import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";
import { useTranslation } from "react-i18next";

interface LanguageContextType {
  currentLanguage: string;
  changeLanguage: (language: string) => void;
  availableLanguages: {
    code: string;
    name: string;
    nativeName: string;
    countries: string[];
  }[];
}

const LanguageContext = createContext<LanguageContextType | undefined>(
  undefined
);

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
};

interface LanguageProviderProps {
  children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({
  children,
}) => {
  const { i18n } = useTranslation();
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language || "en");

  const availableLanguages = [
    {
      code: "en",
      name: "English",
      nativeName: "English",
      countries: [
        "US",
        "GB",
        "CA",
        "AU",
        "NZ",
        "IE",
        "ZA",
        "IN",
        "PK",
        "NG",
        "PH",
        "KE",
        "UG",
        "TZ",
        "ZW",
        "ZM",
        "MW",
        "BW",
        "LS",
        "SZ",
        "NA",
        "GM",
        "SL",
        "LR",
        "GH",
        "CM",
        "NG",
        "BI",
        "RW",
        "TZ",
        "UG",
        "KE",
        "ET",
        "SO",
        "DJ",
        "ER",
        "SD",
        "SS",
        "CF",
        "CG",
        "CD",
        "GA",
        "GQ",
        "ST",
        "AO",
        "MZ",
        "ZW",
        "ZM",
        "MW",
        "BW",
        "LS",
        "SZ",
        "NA",
        "GM",
        "SL",
        "LR",
        "GH",
        "CM",
        "NG",
        "BI",
        "RW",
        "TZ",
        "UG",
        "KE",
        "ET",
        "SO",
        "DJ",
        "ER",
        "SD",
        "SS",
        "CF",
        "CG",
        "CD",
        "GA",
        "GQ",
        "ST",
        "AO",
        "MZ",
      ],
    },
    {
      code: "es",
      name: "Spanish",
      nativeName: "Español",
      countries: [
        "ES",
        "MX",
        "AR",
        "CO",
        "PE",
        "VE",
        "CL",
        "EC",
        "GT",
        "CU",
        "BO",
        "DO",
        "HN",
        "PY",
        "SV",
        "NI",
        "CR",
        "PA",
        "UY",
        "GQ",
        "PH",
        "US",
        "PR",
        "GU",
        "VI",
        "AS",
        "MP",
        "FM",
        "PW",
        "MH",
        "CK",
        "NU",
        "TK",
        "TO",
        "WS",
        "FJ",
        "VU",
        "NC",
        "PF",
        "WF",
        "TV",
        "KI",
        "NR",
        "PG",
        "SB",
        "VU",
        "NC",
        "PF",
        "WF",
        "TV",
        "KI",
        "NR",
        "PG",
        "SB",
      ],
    },
  ];

  const detectUserLanguage = (): string => {
    // First check if user has a saved preference
    const savedLanguage = localStorage.getItem("preferredLanguage");
    if (
      savedLanguage &&
      availableLanguages.some((lang) => lang.code === savedLanguage)
    ) {
      return savedLanguage;
    }

    // Check browser language
    const browserLanguage = navigator.language.split("-")[0];
    if (availableLanguages.some((lang) => lang.code === browserLanguage)) {
      return browserLanguage;
    }

    // Check if user is in a Spanish-speaking country
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;

          // Simple country detection based on coordinates
          // This is a basic implementation - in production you'd use a proper geocoding service
          const isSpanishSpeakingCountry = checkIfSpanishSpeakingCountry(
            latitude,
            longitude
          );
          if (isSpanishSpeakingCountry) {
            changeLanguage("es");
          }
        },
        () => {
          // If geolocation fails, fall back to browser language or default
          const fallbackLanguage = availableLanguages.some(
            (lang) => lang.code === browserLanguage
          )
            ? browserLanguage
            : "en";
          changeLanguage(fallbackLanguage);
        }
      );
    }

    // Default fallback
    return "en";
  };

  const checkIfSpanishSpeakingCountry = (lat: number, lng: number): boolean => {
    // Basic Spanish-speaking country detection
    // This is a simplified version - in production use a proper geocoding API
    const spanishSpeakingRegions = [
      // Spain
      { minLat: 35.9, maxLat: 43.8, minLng: -9.4, maxLng: 3.3 },
      // Mexico
      { minLat: 14.5, maxLat: 32.7, minLng: -118.4, maxLng: -86.7 },
      // Central America
      { minLat: 7.2, maxLat: 18.5, minLng: -92.2, maxLng: -77.1 },
      // South America (Spanish-speaking countries)
      { minLat: -55.0, maxLat: 12.0, minLng: -81.4, maxLng: -34.8 },
      // Caribbean Spanish-speaking countries
      { minLat: 17.7, maxLat: 23.2, minLng: -84.9, maxLng: -61.2 },
    ];

    return spanishSpeakingRegions.some(
      (region) =>
        lat >= region.minLat &&
        lat <= region.maxLat &&
        lng >= region.minLng &&
        lng <= region.maxLng
    );
  };

  const changeLanguage = (language: string) => {
    i18n.changeLanguage(language);
    setCurrentLanguage(language);
    localStorage.setItem("preferredLanguage", language);
  };

  useEffect(() => {
    const detectedLanguage = detectUserLanguage();
    if (detectedLanguage !== currentLanguage) {
      changeLanguage(detectedLanguage);
    }
  }, []);

  const value: LanguageContextType = {
    currentLanguage,
    changeLanguage,
    availableLanguages,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};
