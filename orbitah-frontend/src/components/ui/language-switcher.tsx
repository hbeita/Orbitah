import { useLanguage } from "@/contexts/LanguageContext";
import { Check, ChevronDown } from "lucide-react";
import React, { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

export const LanguageSwitcher: React.FC = () => {
  const { currentLanguage, changeLanguage, availableLanguages } = useLanguage();
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleLanguageChange = (languageCode: string) => {
    changeLanguage(languageCode);
    setIsOpen(false);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const getFlagEmoji = (languageCode: string) => {
    return languageCode === "en" ? "🇺🇸" : languageCode === "es" ? "🇪🇸" : "🌐";
  };

  return (
    <div className="relative z-[9999]" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-center w-10 h-10 p-0 text-white/80 hover:text-white hover:bg-white/20 rounded-lg transition-colors border border-white/20 bg-transparent"
      >
        <span className="text-lg leading-none">
          {getFlagEmoji(currentLanguage)}
        </span>
        <ChevronDown
          className={`h-3 w-3 ml-1 transition-transform ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-gray-900/95 backdrop-blur-md border border-white/20 rounded-lg shadow-lg z-[9999]">
          <div className="py-1">
            {availableLanguages.map((language) => (
              <button
                key={language.code}
                onClick={() => handleLanguageChange(language.code)}
                className={`w-full flex items-center justify-between px-4 py-2 text-sm transition-colors ${
                  currentLanguage === language.code
                    ? "bg-blue-600/30 text-blue-300"
                    : "text-white hover:text-white hover:bg-white/10"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-lg">{getFlagEmoji(language.code)}</span>
                  <div className="flex flex-col items-start">
                    <span className="font-medium">{language.nativeName}</span>
                    <span className="text-xs opacity-70">{language.name}</span>
                  </div>
                </div>
                {currentLanguage === language.code && (
                  <Check className="h-4 w-4 text-blue-300" />
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
