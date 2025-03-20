"""
MockPy - Comprehensive Realistic Data Generation Library

This library provides developers with a tool to generate realistic
and comprehensive mock data for testing, development, and demo purposes.
"""

import random
import string
import datetime
import re
import json
import uuid

from typing import Dict, List, Any, Optional, Union, TypeVar
from dataclasses import dataclass, field
import warnings
import time

try:
    import translators as ts
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False

__version__ = "0.1.0"

T = TypeVar('T')

class MockPyError(Exception):
    """Base exception class for MockPy library"""
    pass

class MockPyLocaleError(MockPyError):
    """Exception for locale-related errors"""
    pass

class MockPyValueError(MockPyError):
    """Exception for value-related errors"""
    pass

@dataclass
class DataRegistry:
    """Registry for data sources"""
    locales: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    custom_providers: Dict[str, Any] = field(default_factory=dict)
    
    @staticmethod
    def load_locale_data(locale_code: str) -> Dict[str, Any]:
        """Load locale data for a specific locale code"""
        locale_data = {}
        
        if locale_code.startswith("tr"):
            locale_data = {
                "first_names": ["Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Zeynep", "Mustafa", "Emine", 
                              "Hüseyin", "İbrahim", "Hatice", "Elif", "Murat", "Hasan", "Merve", "Seda",
                              "Oğuz", "Burak", "Serkan", "Özge", "Ece", "Deniz", "Gül", "Emre", "Kemal",
                              "Tülay", "Selim", "Ebru", "Bilge", "Tolga", "Pınar", "Onur", "Demet", "Cem"],
                "last_names": ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Özdemir", "Aydın", 
                              "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Şen", "Koç", "Özkan",
                              "Yüksel", "Polat", "Aktaş", "Altun", "Taş", "Bulut", "Öztürk", "Kılınç",
                              "Acar", "Avcı", "Tekin", "Yalçın", "Aksoy", "Uçar", "Kaplan", "Turan"],
                "cities": ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Kayseri", 
                          "Trabzon", "Samsun", "Eskişehir", "Gaziantep", "Diyarbakır", "Mersin",
                          "Denizli", "Erzurum", "Malatya", "Kocaeli", "Şanlıurfa", "Aydın", "Hatay",
                          "Manisa", "Balıkesir", "Kahramanmaraş", "Van", "Sakarya", "Tekirdağ"],
                "street_types": ["Sokak", "Caddesi", "Bulvarı", "Meydanı"],
                "domains": [".com.tr", ".com", ".net", ".org", ".biz", ".info"],
                "email_providers": ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"],
                "phone_prefixes": ["530", "532", "535", "536", "537", "538", "539", 
                                 "540", "541", "542", "543", "544", "545", "546", "547", "548", "549",
                                 "505", "506", "507", "551", "552", "553", "554", "555", "559"],
                "currency": {"code": "TRY", "symbol": "₺"},
                "country": "Türkiye",
                "country_code": "TR",
                "language": "Türkçe",
                "timezone": "Europe/Istanbul",
                "iban_prefix": "TR",
                "job_titles": ["Yazılım Mühendisi", "Veri Analisti", "Proje Yöneticisi", "Pazarlama Uzmanı", 
                              "İnsan Kaynakları Uzmanı", "Grafik Tasarımcı", "Sosyal Medya Yöneticisi", 
                              "Muhasebeci", "Satış Temsilcisi", "Müşteri Hizmetleri Temsilcisi",
                              "Sistem Yöneticisi", "Ağ Uzmanı", "Finansal Analist", "İş Geliştirme Uzmanı",
                              "Ürün Müdürü", "İçerik Yazarı", "Dijital Pazarlama Uzmanı", "CEO", "CTO", "CFO"],
                "departments": ["Yazılım", "Pazarlama", "İnsan Kaynakları", "Finans", "Satış", 
                              "Müşteri Hizmetleri", "Ar-Ge", "Operasyon", "Hukuk", "Bilgi Teknolojileri", 
                              "Lojistik", "Üretim", "Kalite Kontrol", "İdari İşler", "Güvenlik"],
                "street_names": ["Atatürk", "Cumhuriyet", "İstiklal", "Barış", "Uğur", "Gül", "Lale", 
                               "Menekşe", "Papatya", "Zambak", "Çınar", "Meşe", "Zeytin", "Palmiye", 
                               "Ağaç", "Gazi", "Yıldırım", "Fatih", "Mimar Sinan", "Yavuz", "Kanuni"],
                "company_suffixes": ["A.Ş.", "Ltd. Şti.", "Holding", "Grup", "Sanayi", "Teknoloji", "Yazılım"],
                "company_sectors": ["Teknoloji", "Yazılım", "Medikal", "İnşaat", "Otomotiv", "Finans", "Gıda",
                                  "Tekstil", "Mobilya", "Enerji", "Eğitim", "Turizm", "Lojistik", "Sağlık"],
                "universities": ["İstanbul Üniversitesi", "ODTÜ", "Boğaziçi Üniversitesi", "İTÜ", 
                               "Ankara Üniversitesi", "Hacettepe Üniversitesi", "Ege Üniversitesi", 
                               "Yıldız Teknik Üniversitesi", "Koç Üniversitesi", "Sabancı Üniversitesi"],
                "degrees": ["Lisans", "Yüksek Lisans", "Doktora", "Önlisans", "Lise"],
                "fields_of_study": ["Bilgisayar Mühendisliği", "Elektrik-Elektronik Mühendisliği", 
                                  "İşletme", "Ekonomi", "Tıp", "Hukuk", "Psikoloji", "Sosyoloji", 
                                  "Makine Mühendisliği", "Mimarlık", "Moleküler Biyoloji ve Genetik",
                                  "Endüstri Mühendisliği", "Fizik", "Kimya", "Matematik"]
            }
        else:  
            locale_data = {
                "first_names": ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Lisa", 
                              "James", "Linda", "William", "Mary", "Richard", "Patricia", "Joseph", "Jennifer",
                              "Thomas", "Elizabeth", "Charles", "Susan", "Christopher", "Jessica", "Daniel", 
                              "Margaret", "Matthew", "Karen", "Anthony", "Nancy", "Mark", "Betty", "Donald", 
                              "Sandra", "Steven", "Ashley", "Paul", "Dorothy", "Andrew", "Kimberly", "Joshua"],
                "last_names": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", 
                              "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Moore", "Jackson",
                              "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", 
                              "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", 
                              "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson"],
                "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
                          "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", 
                          "San Francisco", "Columbus", "Indianapolis", "Seattle", "Denver", "Boston", 
                          "Portland", "Las Vegas", "Nashville", "Detroit", "Baltimore", "Charlotte", 
                          "Memphis", "Atlanta", "Miami", "Tucson", "Sacramento", "Kansas City"],
                "street_types": ["Street", "Avenue", "Boulevard", "Lane", "Road", "Drive", "Court", "Place", 
                              "Circle", "Way", "Highway", "Parkway", "Terrace", "Trail", "Path"],
                "domains": [".com", ".net", ".org", ".io", ".co", ".us", ".info", ".biz"],
                "email_providers": ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", 
                                  "aol.com", "protonmail.com", "mail.com", "zoho.com"],
                "phone_prefixes": ["201", "202", "203", "205", "206", "207", "208", "209", "210", 
                                 "212", "213", "214", "215", "216", "217", "218", "219", "301", 
                                 "302", "303", "304", "305", "307", "308", "309", "310", "312", 
                                 "313", "314", "315", "316", "317", "318", "319", "320", "321"],
                "currency": {"code": "USD", "symbol": "$"},
                "country": "United States",
                "country_code": "US",
                "language": "English",
                "timezone": "America/New_York",
                "iban_prefix": "US",
                "job_titles": ["Software Engineer", "Data Analyst", "Project Manager", "Marketing Specialist", 
                              "HR Manager", "Graphic Designer", "Social Media Manager", 
                              "Accountant", "Sales Representative", "Customer Service Representative",
                              "Systems Administrator", "Network Engineer", "Financial Analyst", 
                              "Business Development Manager", "Product Manager", "Content Writer", 
                              "Digital Marketing Specialist", "CEO", "CTO", "CFO"],
                "departments": ["Engineering", "Marketing", "Human Resources", "Finance", "Sales", 
                              "Customer Support", "R&D", "Operations", "Legal", "IT", 
                              "Logistics", "Production", "Quality Assurance", "Administration", "Security"],
                "street_names": ["Main", "Oak", "Maple", "Washington", "Lincoln", "Park", "Cedar", 
                               "Pine", "Elm", "Lake", "Hill", "River", "Valley", "Forest", 
                               "Meadow", "Jefferson", "Adams", "Madison", "Franklin", "Central"],
                "company_suffixes": ["Inc.", "LLC", "Corp.", "Group", "Industries", "Tech", "Software", "Solutions"],
                "company_sectors": ["Technology", "Software", "Medical", "Construction", "Automotive", "Finance", "Food",
                                  "Textile", "Furniture", "Energy", "Education", "Tourism", "Logistics", "Healthcare"],
                "universities": ["Harvard University", "MIT", "Stanford University", "Yale University", 
                               "Princeton University", "Columbia University", "University of Chicago", 
                               "University of Michigan", "Cornell University", "Duke University"],
                "degrees": ["Bachelor's", "Master's", "PhD", "Associate's", "High School Diploma"],
                "fields_of_study": ["Computer Science", "Electrical Engineering", 
                                  "Business Administration", "Economics", "Medicine", "Law", "Psychology", "Sociology", 
                                  "Mechanical Engineering", "Architecture", "Molecular Biology", 
                                  "Industrial Engineering", "Physics", "Chemistry", "Mathematics"]
            }
        
        return locale_data

class TranslationService:
    """Service for translating data to different languages using free translation APIs"""
    
    def __init__(self):
        self.available = TRANSLATION_AVAILABLE
        self.cache = {}
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'fr') -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'en')
            target_lang: Target language code (default: 'fr')
            
        Returns:
            Translated text or original text if translation is not available
        """
        if not self.available:
            warnings.warn(
                "Translation service is not available. Install 'translators' package for multi-language support.",
                UserWarning
            )
            return text
        
        cache_key = f"{source_lang}:{target_lang}:{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            translation_services = [
                lambda t, s, tg: ts.google(t, s, tg),
                lambda t, s, tg: ts.bing(t, s, tg),
                lambda t, s, tg: ts.deepl(t, s, tg)
            ]
            
            for service in translation_services:
                try:
                    translated = service(text, source_lang, target_lang)
                    if translated and translated != text:
                        self.cache[cache_key] = translated
                        return translated
                except Exception:
                    continue
            
            return text
            
        except Exception as e:
            warnings.warn(f"Translation failed: {str(e)}")
            return text
    
    def translate_list(self, items: List[str], source_lang: str = 'en', target_lang: str = 'fr') -> List[str]:
        """
        Translate a list of strings
        
        Args:
            items: List of strings to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated strings
        """
        return [self.translate(item, source_lang, target_lang) for item in items]
    
    def translate_dict(self, data: Dict[str, Any], source_lang: str = 'en', target_lang: str = 'fr',
                      skip_keys: List[str] = None) -> Dict[str, Any]:
        """
        Translate a dictionary of strings or lists of strings
        
        Args:
            data: Dictionary to translate
            source_lang: Source language code
            target_lang: Target language code
            skip_keys: List of keys to skip translation
            
        Returns:
            Translated dictionary
        """
        skip_keys = skip_keys or []
        result = {}
        
        for key, value in data.items():
            if key in skip_keys:
                result[key] = value
                continue
                
            if isinstance(value, str):
                result[key] = self.translate(value, source_lang, target_lang)
            elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                result[key] = self.translate_list(value, source_lang, target_lang)
            elif isinstance(value, dict):
                result[key] = self.translate_dict(value, source_lang, target_lang, skip_keys)
            else:
                result[key] = value
                
        return result

class DataContainer:
    """Container class for generated data with attribute access"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self._data = data or {}
    
    def __getattr__(self, name):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict) and not isinstance(value, DataContainer):
                self._data[name] = DataContainer(value)
                return self._data[name]
            return value
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __contains__(self, key):
        return key in self._data
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def to_dict(self):
        """Convert container to dictionary"""
        result = {}
        for key, value in self._data.items():
            if isinstance(value, DataContainer):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"

class Provider:
    """Base provider class responsible for data generation"""
    
    def __init__(self, mockpy_instance):
        self.mockpy = mockpy_instance
    
    @property
    def random(self):
        return self.mockpy._random
    
    @property
    def locale_data(self):
        return self.mockpy._locale_data

class PersonProvider(Provider):
    """Provider for person-related data"""
    
    def name(self, gender: str = None) -> str:
        """Generate a random first name"""
        return self.random.choice(self.locale_data["first_names"])
    
    def first_name(self, gender: str = None) -> str:
        """Generate a random first name"""
        return self.name(gender)
    
    def last_name(self) -> str:
        """Generate a random last name"""
        return self.random.choice(self.locale_data["last_names"])
    
    def full_name(self, gender: str = None) -> str:
        """Generate a random full name"""
        return f"{self.first_name(gender)} {self.last_name()}"
    
    def gender(self) -> str:
        """Generate a random gender"""
        return self.random.choice(["male", "female", "non-binary"])
    
    def birth_date(self, min_age: int = 18, max_age: int = 80) -> datetime.date:
        """
        Generate a random birth date within the given age range
        
        Args:
            min_age: Minimum age in years
            max_age: Maximum age in years
            
        Returns:
            Random birth date as a datetime.date object
        """
        today = datetime.date.today()
        age = self.random.randint(min_age, max_age)
        birth_year = today.year - age
        
        birth_date = datetime.date(birth_year, 1, 1)
        
        if birth_year % 4 == 0 and (birth_year % 100 != 0 or birth_year % 400 == 0):
            days_in_year = 366
        else:
            days_in_year = 365
        
        random_day = self.random.randint(1, days_in_year)
        birth_date = birth_date + datetime.timedelta(days=random_day-1)
        
        return birth_date
    
    def age(self, min_age: int = 18, max_age: int = 80) -> int:
        """Generate a random age"""
        return self.random.randint(min_age, max_age)
    
    def phone_number(self, formatted: bool = True) -> str:
        """
        Generate a random phone number
        
        Args:
            formatted: Whether to format the phone number with spaces/dashes
            
        Returns:
            A random phone number string
        """
        country_code = self.mockpy.locale.split("_")[1] if "_" in self.mockpy.locale else "US"
        
        if country_code == "TR":
            prefix = self.random.choice(self.locale_data["phone_prefixes"])
            subscriber = ''.join(self.random.choices(string.digits, k=7))
            
            if formatted:
                return f"+90 {prefix} {subscriber[:3]} {subscriber[3:]}"
            else:
                return f"+90{prefix}{subscriber}"
        else:
            area_code = self.random.randint(200, 999)
            exchange = self.random.randint(200, 999)
            subscriber = self.random.randint(1000, 9999)
            
            if formatted:
                return f"+1 ({area_code}) {exchange}-{subscriber}"
            else:
                return f"+1{area_code}{exchange}{subscriber}"
    
    def email(self, name: str = None, domain: str = None) -> str:
        """
        Generate an email address
        
        Args:
            name: Optional name to use as the username part
            domain: Optional domain name
            
        Returns:
            A random email address
        """
        if name is None:
            first = self.first_name().lower()
            last = self.last_name().lower()
            
            patterns = [
                lambda f, l: f"{f}",
                lambda f, l: f"{f}.{l}",
                lambda f, l: f"{f}{l}",
                lambda f, l: f"{f[0]}{l}",
                lambda f, l: f"{f}{l[0]}"
            ]
            
            name = self.random.choice(patterns)(first, last)
            
            if self.random.random() < 0.3:
                name += str(self.random.randint(1, 9999))
        
        if domain is None:
            domain = self.random.choice(self.locale_data["email_providers"])
        
        return f"{name}@{domain}"
    
    def person(self, include_id: bool = True, include_address: bool = False,
              min_age: int = 18, max_age: int = 80) -> DataContainer:
        """
        Generate complete person data
        
        Args:
            include_id: Whether to include a UUID
            include_address: Whether to include an address
            min_age: Minimum age for the person
            max_age: Maximum age for the person
            
        Returns:
            A DataContainer with the person's information
        """
        gender = self.gender()
        first_name = self.first_name(gender)
        last_name = self.last_name()
        full_name = f"{first_name} {last_name}"
        
        birth_date = self.birth_date(min_age, max_age)
        age = datetime.date.today().year - birth_date.year
        
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "gender": gender,
            "birth_date": birth_date.isoformat(),
            "age": age,
            "email": self.email(f"{first_name.lower()}.{last_name.lower()}"),
            "phone": self.phone_number(),
            "nationality": self.locale_data["country"],
            "language": self.locale_data["language"]
        }
        
        if include_id:
            data["id"] = str(uuid.uuid4())
        
        if include_address:
            data["address"] = self.mockpy.address.address().to_dict()
        
        return DataContainer(data)
    
    def job_title(self) -> str:
        """Generate a random job title"""
        return self.random.choice(self.locale_data["job_titles"])
    
    def department(self) -> str:
        """Generate a random department name"""
        return self.random.choice(self.locale_data["departments"])
    
    def education(self) -> DataContainer:
        """Generate random education information"""
        university = self.random.choice(self.locale_data["universities"])
        degree = self.random.choice(self.locale_data["degrees"])
        field = self.random.choice(self.locale_data["fields_of_study"])
        
        current_year = datetime.date.today().year
        graduation_year = current_year - self.random.randint(3, 50)
        
        data = {
            "university": university,
            "degree": degree,
            "field_of_study": field,
            "graduation_year": graduation_year
        }
        
        return DataContainer(data)

class AddressProvider(Provider):
    """Provider for address-related data"""
    
    def street_name(self) -> str:
        """Generate a random street name"""
        base_name = self.random.choice(self.locale_data["street_names"])
        return f"{base_name} {self.random.choice(self.locale_data['street_types'])}"
    
    def street_number(self) -> int:
        """Generate a random street/building number"""
        return self.random.randint(1, 999)
    
    def street_address(self) -> str:
        """Generate a full street address (number + street)"""
        return f"{self.street_number()} {self.street_name()}"
    
    def city(self) -> str:
        """Generate a random city name"""
        return self.random.choice(self.locale_data["cities"])
    
    def postal_code(self) -> str:
        """Generate a random postal code"""
        if self.mockpy.locale.startswith("tr"):
            return ''.join(self.random.choices(string.digits, k=5))
        else:
            return ''.join(self.random.choices(string.digits, k=5))
    
    def country(self) -> str:
        """Return the country name for the current locale"""
        return self.locale_data["country"]
    
    def address(self) -> DataContainer:
        """Generate a complete address"""
        street = self.street_address()
        city = self.city()
        postal = self.postal_code()
        country = self.country()
        
        data = {
            "street": street,
            "city": city,
            "postal_code": postal,
            "country": country,
            "formatted": f"{street}\n{city}, {postal}\n{country}"
        }
        
        return DataContainer(data)
    
    def coordinates(self) -> Dict[str, float]:
        """
        Generate random GPS coordinates
        
        Returns:
            A dict with 'latitude' and 'longitude' keys
        """
        if self.mockpy.locale.startswith("tr"):
            lat = self.random.uniform(36.0, 42.0)
            lng = self.random.uniform(26.0, 45.0)
        else:
            lat = self.random.uniform(24.0, 49.0)
            lng = self.random.uniform(-125.0, -66.0)
        
        lat = round(lat, 6)
        lng = round(lng, 6)
        
        return {"latitude": lat, "longitude": lng}

class CompanyProvider(Provider):
    """Provider for company and business-related data"""
    
    def _generate_company_name(self) -> str:
        """Generate a company name"""
        patterns = [
            lambda: self.random.choice(self.locale_data["last_names"]),
            lambda: ''.join(self.random.choices(string.ascii_uppercase, k=self.random.randint(2, 4))),
            lambda: f"{self.random.choice(self.locale_data['last_names'])}-{self.random.choice(self.locale_data['last_names'])}"
        ]
        
        return self.random.choice(patterns)()
    
    def _company_suffix(self) -> str:
        """Generate a company type/suffix"""
        return self.random.choice(self.locale_data["company_suffixes"])
    
    def company_name(self) -> str:
        """Generate a full company name"""
        name = self._generate_company_name()
        
        if self.random.random() < 0.4:
            name = f"{name} {self.random.choice(self.locale_data['company_sectors'])}"
        
        suffix = self._company_suffix()
        
        return f"{name} {suffix}"
    
    def catch_phrase(self) -> str:
        """Generate a company slogan"""
        if self.mockpy.locale.startswith("tr"):
            phrases = [
                "Kalitede öncü, hizmette lider.",
                "Geleceği şekillendiriyoruz.",
                "Sizin için çalışıyoruz.",
                "Yenilikçi çözümler, mutlu müşteriler.",
                "Güvenilir hizmet, garantili memnuniyet."
            ]
        else:
            phrases = [
                "Innovating for a better tomorrow.",
                "Excellence in everything we do.",
                "Building the future today.",
                "Customer satisfaction is our priority.",
                "Leading the industry with innovative solutions."
            ]
        
        return self.random.choice(phrases)
    
    def industry(self) -> str:
        """Generate a random industry/sector"""
        industries = [
            "Technology", "Healthcare", "Finance", "Manufacturing", "Retail", 
            "Education", "Energy", "Entertainment", "Transportation", "Hospitality"
        ]
        return self.random.choice(industries)
    
    def company_type(self) -> str:
        """Generate a company type"""
        types = ["Startup", "Corporation", "Non-Profit", "Government", "Partnership", "Sole Proprietorship"]
        return self.random.choice(types)
    
    def website(self, company_name: str = None) -> str:
        """
        Generate a company website URL
        
        Args:
            company_name: Optional company name to use
            
        Returns:
            A website URL
        """
        if company_name is None:
            company_name = self._generate_company_name()
        
        domain_name = company_name.lower()
        domain_name = re.sub(r'[^\w\s-]', '', domain_name)
        domain_name = re.sub(r'[\s-]+', '-', domain_name)
        domain_name = domain_name.strip('-')
        
        tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u'}
        for tr_char, en_char in tr_chars.items():
            domain_name = domain_name.replace(tr_char, en_char)
        
        domain_suffix = self.random.choice(self.locale_data["domains"])
        
        return f"www.{domain_name}{domain_suffix}"
    
    def company(self) -> DataContainer:
        """Generate complete company data"""
        name = self.company_name()
        data = {
            "name": name,
            "legal_name": name,
            "catch_phrase": self.catch_phrase(),
            "industry": self.industry(),
            "type": self.company_type(),
            "website": self.website(name),
            "employees": self.random.randint(5, 10000),
            "founded": self.random.randint(1950, datetime.date.today().year - 1),
            "address": self.mockpy.address.address().to_dict()
        }
        
        return DataContainer(data)

class FinanceProvider(Provider):
    """Provider for financial data"""
    
    def credit_card(self) -> DataContainer:
        """Generate credit card information"""
        card_types = {
            "VISA": {"prefix": ["4"], "length": 16},
            "Mastercard": {"prefix": ["51", "52", "53", "54", "55"], "length": 16},
            "American Express": {"prefix": ["34", "37"], "length": 15}
        }
        
        card_type = self.random.choice(list(card_types.keys()))
        card_info = card_types[card_type]
        
        prefix = self.random.choice(card_info["prefix"])
        length = card_info["length"]
        
        remaining_length = length - len(prefix)
        number = prefix + ''.join(self.random.choices(string.digits, k=remaining_length - 1))
        
        digits = [int(d) for d in number]
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        checksum = sum(digits) % 10
        if checksum != 0:
            checksum = 10 - checksum
        
        number += str(checksum)
        
        today = datetime.date.today()
        exp_year = today.year + self.random.randint(1, 4)
        exp_month = self.random.randint(1, 12)
        
        cvv_length = 4 if card_type == "American Express" else 3
        cvv = ''.join(self.random.choices(string.digits, k=cvv_length))
        
        data = {
            "type": card_type,
            "number": number,
            "formatted_number": self._format_cc_number(number, card_type),
            "expiration": f"{exp_month:02d}/{exp_year % 100:02d}",
            "cvv": cvv,
            "holder_name": f"{self.random.choice(self.locale_data['first_names'])} {self.random.choice(self.locale_data['last_names'])}"
        }
        
        return DataContainer(data)
    
    def _format_cc_number(self, number: str, card_type: str) -> str:
        """Format credit card number for display"""
        if card_type == "American Express":
            return f"{number[:4]} {number[4:10]} {number[10:]}"
        else:
            return f"{number[:4]} {number[4:8]} {number[8:12]} {number[12:]}"
    
    def iban(self) -> str:
        """Generate a random IBAN number"""
        country_code = self.locale_data["iban_prefix"]
        
        if country_code == "TR":
            bank_code = ''.join(self.random.choices(string.digits, k=5))
            branch_code = ''.join(self.random.choices(string.digits, k=1))
            account_number = ''.join(self.random.choices(string.digits, k=16))
            
            check_digits = "00"
            
            return f"{country_code}{check_digits}{bank_code}{branch_code}{account_number}"
        else:
            check_digits = "00"
            bank_code = ''.join(self.random.choices(string.digits, k=4))
            account_number = ''.join(self.random.choices(string.digits, k=16))
            
            return f"{country_code}{check_digits}{bank_code}{account_number}"
    
    def bank_account(self) -> DataContainer:
        """Generate bank account information"""
        account_number = ''.join(self.random.choices(string.digits, k=10))
        routing_number = ''.join(self.random.choices(string.digits, k=9))
        
        data = {
            "account_name": f"{self.random.choice(self.locale_data['first_names'])} {self.random.choice(self.locale_data['last_names'])}",
            "account_number": account_number,
            "routing_number": routing_number,
            "iban": self.iban(),
            "swift_bic": ''.join(self.random.choices(string.ascii_uppercase, k=8)),
            "bank_name": f"{self.random.choice(self.locale_data['last_names'])} Bank"
        }
        
        return DataContainer(data)
    
    def price(self, min_price: float = 1.0, max_price: float = 1000.0, 
             decimals: int = 2, symbol: bool = True) -> str:
        """
        Generate a random price
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            decimals: Number of decimal places
            symbol: Whether to include the currency symbol
            
        Returns:
            A formatted price string
        """
        amount = round(self.random.uniform(min_price, max_price), decimals)
        
        if symbol:
            currency_symbol = self.locale_data["currency"]["symbol"]
            if self.mockpy.locale.startswith("tr"):
                return f"{amount:.{decimals}f} {currency_symbol}"
            else:
                return f"{currency_symbol}{amount:.{decimals}f}"
        else:
            return f"{amount:.{decimals}f}"
    
    def transaction(self, min_amount: float = 1.0, max_amount: float = 1000.0) -> DataContainer:
        """Generate financial transaction information"""
        amount = round(self.random.uniform(min_amount, max_amount), 2)
        transaction_types = ["deposit", "withdrawal", "transfer", "payment", "refund"]
        
        today = datetime.date.today()
        days_ago = self.random.randint(0, 365)
        transaction_date = today - datetime.timedelta(days=days_ago)
        
        data = {
            "id": str(uuid.uuid4()),
            "date": transaction_date.isoformat(),
            "amount": amount,
            "formatted_amount": self.price(amount, amount),
            "type": self.random.choice(transaction_types),
            "status": self.random.choice(["completed", "pending", "failed"]),
            "description": f"Transaction #{self.random.randint(10000, 99999)}"
        }
        
        return DataContainer(data)

class InternetProvider(Provider):
    """Provider for internet and technology-related data"""
    
    def user_name(self, name: str = None) -> str:
        """
        Generate a username
        
        Args:
            name: Optional name to base the username on
            
        Returns:
            A username string
        """
        if name is None:
            first = self.random.choice(self.locale_data["first_names"]).lower()
            last = self.random.choice(self.locale_data["last_names"]).lower()
            
            patterns = [
                lambda f, l: f"{f}",
                lambda f, l: f"{f}{self.random.randint(1, 999)}",
                lambda f, l: f"{f}_{l}",
                lambda f, l: f"{f}.{l}",
                lambda f, l: f"{f[0]}{l}",
                lambda f, l: f"{f}{l[0]}",
                lambda f, l: f"{f}{self.random.choice(['_', '.'])}{l}"
            ]
            
            name = self.random.choice(patterns)(first, last)
        
        tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u'}
        for tr_char, en_char in tr_chars.items():
            name = name.replace(tr_char, en_char)
        
        return name
    
    def password(self, length: int = 12, special_chars: bool = True, 
               digits: bool = True, upper: bool = True) -> str:
        """
        Generate a secure password
        
        Args:
            length: Length of the password
            special_chars: Whether to include special characters
            digits: Whether to include digits
            upper: Whether to include uppercase letters
            
        Returns:
            A password string
        """
        chars = string.ascii_lowercase
        if upper:
            chars += string.ascii_uppercase
        if digits:
            chars += string.digits
        if special_chars:
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
        
        password = ''.join(self.random.choices(chars, k=length))
        
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password) if upper else True
        has_digit = any(c.isdigit() for c in password) if digits else True
        has_special = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password) if special_chars else True
        
        if not (has_lower and has_upper and has_digit and has_special):
            return self.password(length, special_chars, digits, upper)
        
        return password
    
    def domain_name(self) -> str:
        """Generate a random domain name"""
        company = self.random.choice(self.locale_data["last_names"]).lower()
        tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u'}
        for tr_char, en_char in tr_chars.items():
            company = company.replace(tr_char, en_char)
        
        suffix = self.random.choice(self.locale_data["domains"])
        return f"{company}{suffix}"
    
    def url(self, protocol: str = "https") -> str:
        """Generate a random URL"""
        domain = self.domain_name()
        
        paths = ["", "index.html", "about", "contact", "products", "services", "blog"]
        path = self.random.choice(paths)
        
        url = f"{protocol}://{domain}"
        if path:
            url += f"/{path}"
        
        return url
    
    def ip_v4(self) -> str:
        """Generate a random IPv4 address"""
        return '.'.join(str(self.random.randint(0, 255)) for _ in range(4))
    
    def ip_v6(self) -> str:
        """Generate a random IPv6 address"""
        return ':'.join(''.join(self.random.choices('0123456789abcdef', k=4)) for _ in range(8))
    
    def mac_address(self) -> str:
        """Generate a random MAC address"""
        return ':'.join(''.join(self.random.choices('0123456789abcdef', k=2)) for _ in range(6))
    
    def user_agent(self) -> str:
        """Generate a random user agent string"""
        browsers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
        ]
        return self.random.choice(browsers)

class LoremProvider(Provider):
    """Provider for text and content generation"""
    
    def word(self) -> str:
        """Generate a single lorem ipsum word"""
        words = [
            "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
            "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
            "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud", "exercitation",
            "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat",
            "duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit",
            "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur", "excepteur", "sint",
            "occaecat", "cupidatat", "non", "proident", "sunt", "in", "culpa", "qui", "officia",
            "deserunt", "mollit", "anim", "id", "est", "laborum"
        ]
        return self.random.choice(words)
    
    def words(self, num_words: int = 5) -> str:
        """
        Generate multiple lorem ipsum words
        
        Args:
            num_words: Number of words to generate
            
        Returns:
            A string of space-separated words
        """
        return ' '.join(self.word() for _ in range(num_words))
    
    def sentence(self, min_words: int = 4, max_words: int = 12) -> str:
        """
        Generate a lorem ipsum sentence
        
        Args:
            min_words: Minimum number of words
            max_words: Maximum number of words
            
        Returns:
            A sentence string with capitalization and period
        """
        num_words = self.random.randint(min_words, max_words)
        sentence = self.words(num_words)
        return sentence[0].upper() + sentence[1:] + "."
    
    def sentences(self, num_sentences: int = 3) -> str:
        """
        Generate multiple lorem ipsum sentences
        
        Args:
            num_sentences: Number of sentences to generate
            
        Returns:
            A string of sentences separated by spaces
        """
        return ' '.join(self.sentence() for _ in range(num_sentences))
    
    def paragraph(self, min_sentences: int = 3, max_sentences: int = 7) -> str:
        """
        Generate a lorem ipsum paragraph
        
        Args:
            min_sentences: Minimum number of sentences
            max_sentences: Maximum number of sentences
            
        Returns:
            A paragraph as a string
        """
        num_sentences = self.random.randint(min_sentences, max_sentences)
        return self.sentences(num_sentences)
    
    def paragraphs(self, num_paragraphs: int = 3, separator: str = "\n\n") -> str:
        """
        Generate multiple lorem ipsum paragraphs
        
        Args:
            num_paragraphs: Number of paragraphs to generate
            separator: String to separate paragraphs
            
        Returns:
            A string of paragraphs separated by the separator
        """
        return separator.join(self.paragraph() for _ in range(num_paragraphs))

class DateTimeProvider(Provider):
    """Provider for date and time related data"""
    
    def date_between(self, start_date: Union[str, datetime.date], 
                   end_date: Union[str, datetime.date]) -> datetime.date:
        """
        Generate a random date between two dates
        
        Args:
            start_date: Start date (string in ISO format or datetime.date)
            end_date: End date (string in ISO format or datetime.date)
            
        Returns:
            A random date between start_date and end_date
        """
        if isinstance(start_date, str):
            start_date = datetime.date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.date.fromisoformat(end_date)
        
        delta = (end_date - start_date).days
        if delta < 0:
            raise ValueError("End date must be after start date")
        
        offset = self.random.randint(0, delta)
        return start_date + datetime.timedelta(days=offset)
    
    def date_this_year(self) -> datetime.date:
        """Generate a random date in the current year"""
        today = datetime.date.today()
        start_date = datetime.date(today.year, 1, 1)
        end_date = datetime.date(today.year, 12, 31)
        return self.date_between(start_date, end_date)
    
    def date_this_month(self) -> datetime.date:
        """Generate a random date in the current month"""
        today = datetime.date.today()
        start_date = datetime.date(today.year, today.month, 1)
        
        if today.month == 12:
            next_month = datetime.date(today.year + 1, 1, 1)
        else:
            next_month = datetime.date(today.year, today.month + 1, 1)
        end_date = next_month - datetime.timedelta(days=1)
        
        return self.date_between(start_date, end_date)
    
    def time(self) -> datetime.time:
        """Generate a random time"""
        return datetime.time(
            hour=self.random.randint(0, 23),
            minute=self.random.randint(0, 59),
            second=self.random.randint(0, 59)
        )
    
    def datetime_between(self, start_date: Union[str, datetime.datetime],
                        end_date: Union[str, datetime.datetime]) -> datetime.datetime:
        """
        Generate a random datetime between two datetimes
        
        Args:
            start_date: Start datetime (string in ISO format or datetime.datetime)
            end_date: End datetime (string in ISO format or datetime.datetime)
            
        Returns:
            A random datetime between start_date and end_date
        """
        if isinstance(start_date, str):
            start_date = datetime.datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.datetime.fromisoformat(end_date)
        
        delta = (end_date - start_date).total_seconds()
        if delta < 0:
            raise ValueError("End datetime must be after start datetime")
        
        offset = self.random.randint(0, int(delta))
        return start_date + datetime.timedelta(seconds=offset)
    
    def iso8601(self, tzinfo=None) -> str:
        """Generate a random datetime in ISO 8601 format"""
        year = self.random.randint(1970, datetime.date.today().year)
        month = self.random.randint(1, 12)
        day = self.random.randint(1, 28)
        hour = self.random.randint(0, 23)
        minute = self.random.randint(0, 59)
        second = self.random.randint(0, 59)
        microsecond = self.random.randint(0, 999999)
        
        dt = datetime.datetime(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo)
        return dt.isoformat()

class MockPy:
    """Main MockPy class - central API for data generation"""
    
    def __init__(self, locale: str = "en_US", seed: Optional[int] = None):
        """
        Initialize MockPy instance
        
        Args:
            locale: Locale code to use (e.g., "tr_TR", "en_US")
            seed: Random seed for reproducible data generation
        """
        self.locale = locale
        self._seed = seed if seed is not None else int(time.time() * 1000) & 0xFFFFFFFF
        self._random = random.Random(self._seed)
        
        self._data_registry = DataRegistry()
        self._translation_service = TranslationService()
        self._locale_data = self._load_locale_data(locale)
        
        self._init_providers()
    
    def _load_locale_data(self, locale: str) -> Dict[str, Any]:
        """
        Load locale data with translation support
        
        Args:
            locale: Locale code
            
        Returns:
            Dictionary with locale data
        """
        if locale in self._data_registry.locales:
            return self._data_registry.locales[locale]
        
        if locale.startswith("en") or locale.startswith("tr"):
            locale_data = self._data_registry.load_locale_data(locale)
            self._data_registry.locales[locale] = locale_data
            return locale_data
        
        warnings.warn(
            f"No built-in data for locale '{locale}'. Deriving from English with translation.",
            UserWarning
        )
        
        source_locale = "en_US"
        source_data = self._data_registry.load_locale_data(source_locale)
        
        if not self._translation_service.available:
            warnings.warn(
                "Translation service not available. Install 'translators' package for better multi-language support.",
                UserWarning
            )
            self._data_registry.locales[locale] = source_data
            return source_data
        
        lang_code = locale.split("_")[0] if "_" in locale else locale
        
        try:
            skip_keys = ["email_providers", "domains", "iban_prefix", "phone_prefixes", "timezone", 
                       "currency", "country_code"]
            
            translated_data = self._translation_service.translate_dict(
                source_data, 
                source_lang='en', 
                target_lang=lang_code,
                skip_keys=skip_keys
            )
            
            self._data_registry.locales[locale] = translated_data
            return translated_data
            
        except Exception as e:
            warnings.warn(f"Translation failed: {str(e)}. Using English data instead.")
            self._data_registry.locales[locale] = source_data
            return source_data
    
    def _init_providers(self):
        """Initialize all data providers"""
        self.person = PersonProvider(self)
        self.address = AddressProvider(self)
        self.company = CompanyProvider(self)
        self.finance = FinanceProvider(self)
        self.internet = InternetProvider(self)
        self.lorem = LoremProvider(self)
        self.datetime = DateTimeProvider(self)
        
        for provider_name, provider_class in self._data_registry.custom_providers.items():
            setattr(self, provider_name, provider_class(self))
    
    def seed(self, seed_value: int) -> None:
        """Set the random seed for reproducible data generation"""
        self._seed = seed_value
        self._random = random.Random(seed_value)
    
    def random_element(self, elements: List[Any]) -> Any:
        """Select a random element from a list"""
        return self._random.choice(elements)
    
    def add_provider(self, provider_name: str, provider_class: type) -> None:
        """
        Add a new data provider
        
        Args:
            provider_name: Name for the provider
            provider_class: Provider class (must inherit from Provider)
        """
        if not issubclass(provider_class, Provider):
            raise MockPyValueError(f"Provider class must inherit from Provider: {provider_class}")
        
        self._data_registry.custom_providers[provider_name] = provider_class
        setattr(self, provider_name, provider_class(self))
    
    def generate_dataset(self, schema: Dict[str, Any], count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate a dataset based on a schema
        
        Args:
            schema: Schema definition
            count: Number of items to generate
            
        Returns:
            List of generated data items
        """
        result = []
        for _ in range(count):
            item = {}
            for field_name, field_type in schema.items():
                item[field_name] = self._generate_field(field_type)
            result.append(item)
        return result
    
    def _generate_field(self, field_type: Union[str, Dict[str, Any]]) -> Any:
        """
        Generate a field value based on the field type
        
        Args:
            field_type: Field type definition (string or dict)
            
        Returns:
            Generated field value
        """
        if isinstance(field_type, str):
            parts = field_type.split('.')
            
            if len(parts) == 2:
                provider_name, method_name = parts
                provider = getattr(self, provider_name, None)
                if provider is None:
                    raise MockPyValueError(f"Unknown provider: {provider_name}")
                
                method = getattr(provider, method_name, None)
                if method is None:
                    raise MockPyValueError(f"Unknown method {method_name} in provider {provider_name}")
                
                return method()
            else:
                if field_type == "person":
                    return self.person.person()
                elif field_type == "address":
                    return self.address.address()
                elif field_type == "company":
                    return self.company.company()
                elif field_type == "credit_card":
                    return self.finance.credit_card()
                elif field_type == "bank_account":
                    return self.finance.bank_account()
                
                for provider_name in dir(self):
                    provider = getattr(self, provider_name)
                    if isinstance(provider, Provider):
                        method = getattr(provider, field_type, None)
                        if method and callable(method):
                            return method()
                
                raise MockPyValueError(f"Unknown field type: {field_type}")
        elif isinstance(field_type, dict):
            if "type" in field_type:
                type_name = field_type["type"]
                
                if type_name == "choice":
                    return self._random.choice(field_type["choices"])
                elif type_name == "integer":
                    min_val = field_type.get("min", 0)
                    max_val = field_type.get("max", 100)
                    return self._random.randint(min_val, max_val)
                elif type_name == "float":
                    min_val = field_type.get("min", 0.0)
                    max_val = field_type.get("max", 1.0)
                    precision = field_type.get("precision", 2)
                    value = self._random.uniform(min_val, max_val)
                    return round(value, precision)
                elif type_name == "date":
                    start_date = field_type.get("start", "2000-01-01")
                    end_date = field_type.get("end", "2023-12-31")
                    
                    return self.datetime.date_between(start_date, end_date).isoformat()
                elif type_name == "datetime":
                    start_date = field_type.get("start", "2000-01-01T00:00:00")
                    end_date = field_type.get("end", "2023-12-31T23:59:59")
                    
                    return self.datetime.datetime_between(start_date, end_date).isoformat()
                elif type_name == "lorem":
                    words = field_type.get("words", None)
                    if words:
                        return self.lorem.words(words)
                    
                    sentences = field_type.get("sentences", None)
                    if sentences:
                        return self.lorem.sentences(sentences)
                    
                    paragraphs = field_type.get("paragraphs", 1)
                    return self.lorem.paragraphs(paragraphs)
                elif type_name.startswith("provider."):
                    _, provider_name, method_name = type_name.split('.')
                    provider = getattr(self, provider_name, None)
                    if provider is None:
                        raise MockPyValueError(f"Unknown provider: {provider_name}")
                    
                    method = getattr(provider, method_name, None)
                    if method is None:
                        raise MockPyValueError(f"Unknown method {method_name} in provider {provider_name}")
                    
                    args = field_type.get("args", [])
                    kwargs = {k: v for k, v in field_type.items() if k not in ["type", "args"]}
                    
                    return method(*args, **kwargs)
            else:
                result = {}
                for key, value in field_type.items():
                    result[key] = self._generate_field(value)
                return result
        
        return None

class DjangoUtils:
    """Helper class for Django integration"""
    
    @staticmethod
    def generate_model_instances(model_class, count=1, locale="en_US", seed=None, **field_overrides):
        """Generate instances of a Django model"""
        try:
            from django.db.models import Model
            if not issubclass(model_class, Model):
                raise ValueError("model_class must be a Django Model class")
        except ImportError:
            raise ImportError("Django is not installed. Install Django to use this feature.")
        
        mock = MockPy(locale=locale, seed=seed)
        instances = []
        
        for _ in range(count):
            instance = model_class()
            
            for field in model_class._meta.fields:
                if field.name in field_overrides:
                    setattr(instance, field.name, field_overrides[field.name])
                else:
                    if field.primary_key and field.auto_created:
                        continue
                    
                    value = DjangoUtils._generate_value_for_field(field, mock)
                    if value is not None:
                        setattr(instance, field.name, value)
            
            instances.append(instance)
        
        return instances
    
    @staticmethod
    def _generate_value_for_field(field, mock):
        """Generate value for a Django model field"""
        field_class = field.__class__.__name__
        field_name = field.name.lower()
        
        if field.primary_key:
            return None
        
        if field_class in ['CharField', 'TextField']:
            if 'name' in field_name:
                return mock.person.full_name()
            elif 'address' in field_name:
                return mock.address.street_address()
            elif 'city' in field_name:
                return mock.address.city()
            elif 'email' in field_name:
                return mock.person.email()
            elif 'phone' in field_name:
                return mock.person.phone_number()
            elif 'company' in field_name:
                return mock.company.company_name()
            else:
                max_length = getattr(field, 'max_length', 100)
                return ''.join(mock._random.choices(string.ascii_letters + string.digits, k=mock._random.randint(10, max_length)))
        
        elif field_class in ['IntegerField', 'PositiveIntegerField', 'SmallIntegerField']:
            if 'age' in field_name:
                return mock._random.randint(18, 80)
            elif 'year' in field_name:
                return mock._random.randint(1900, datetime.date.today().year)
            elif 'price' in field_name or 'amount' in field_name:
                return mock._random.randint(1, 10000)
            else:
                return mock._random.randint(1, 1000)
        
        elif field_class in ['DecimalField', 'FloatField']:
            if 'price' in field_name or 'amount' in field_name:
                return round(mock._random.uniform(1, 1000), 2)
            else:
                return round(mock._random.uniform(0, 100), 2)
        
        elif field_class in ['DateField', 'DateTimeField']:
            days = mock._random.randint(0, 5 * 365)
            date_value = datetime.date.today() - datetime.timedelta(days=days)
            
            if field_class == 'DateTimeField':
                time_value = datetime.time(
                    hour=mock._random.randint(0, 23),
                    minute=mock._random.randint(0, 59),
                    second=mock._random.randint(0, 59)
                )
                return datetime.datetime.combine(date_value, time_value)
            else:
                return date_value
        
        elif field_class == 'BooleanField':
            return mock._random.choice([True, False])
        
        elif field_class == 'EmailField':
            return mock.person.email()
        
        elif field_class == 'URLField':
            return mock.internet.url()
        
        elif field_class == 'IPAddressField':
            return mock.internet.ip_v4()
        
        return None

class FlaskUtils:
    """Helper class for Flask integration"""
    
    @staticmethod
    def generate_request_data(schema, locale="en_US", seed=None):
        """Generate data for Flask request"""
        mock = MockPy(locale=locale, seed=seed)
        return mock.generate_dataset(schema, count=1)[0]

class SQLAlchemyUtils:
    """Helper class for SQLAlchemy integration"""
    
    @staticmethod
    def generate_model_instances(model_class, count=1, locale="en_US", seed=None, **field_overrides):
        """Generate instances of a SQLAlchemy model"""
        try:
            from sqlalchemy.ext.declarative import DeclarativeMeta
            if not isinstance(model_class, DeclarativeMeta):
                raise ValueError("model_class must be a SQLAlchemy model class")
        except ImportError:
            raise ImportError("SQLAlchemy is not installed. Install SQLAlchemy to use this feature.")
        
        mock = MockPy(locale=locale, seed=seed)
        instances = []
        
        columns = {column.name: column for column in model_class.__table__.columns}
        
        for _ in range(count):
            instance_data = {}
            
            for column_name, column in columns.items():
                if column_name in field_overrides:
                    instance_data[column_name] = field_overrides[column_name]
                else:
                    if column.primary_key and column.autoincrement:
                        continue
                    
                    value = SQLAlchemyUtils._generate_value_for_column(column, mock)
                    if value is not None:
                        instance_data[column_name] = value
            
            instance = model_class(**instance_data)
            instances.append(instance)
        
        return instances
    
    @staticmethod
    def _generate_value_for_column(column, mock):
        """Generate value for a SQLAlchemy column"""
        column_type = str(column.type)
        column_name = column.name.lower()
        
        if 'int' in column_type:
            if 'age' in column_name:
                return mock._random.randint(18, 80)
            elif 'year' in column_name:
                return mock._random.randint(1900, datetime.date.today().year)
            elif 'price' in column_name or 'amount' in column_name:
                return mock._random.randint(1, 10000)
            else:
                return mock._random.randint(1, 1000)
        
        elif 'float' in column_type or 'numeric' in column_type or 'decimal' in column_type:
            if 'price' in column_name or 'amount' in column_name:
                return round(mock._random.uniform(1, 1000), 2)
            else:
                return round(mock._random.uniform(0, 100), 2)
        
        elif 'varchar' in column_type or 'text' in column_type or 'char' in column_type or 'string' in column_type:
            if 'name' in column_name:
                if 'first' in column_name:
                    return mock.person.first_name()
                elif 'last' in column_name:
                    return mock.person.last_name()
                else:
                    return mock.person.full_name()
            elif 'address' in column_name:
                return mock.address.street_address()
            elif 'city' in column_name:
                return mock.address.city()
            elif 'email' in column_name:
                return mock.person.email()
            elif 'phone' in column_name:
                return mock.person.phone_number()
            elif 'company' in column_name:
                return mock.company.company_name()
            elif 'password' in column_name:
                return mock.internet.password()
            elif 'username' in column_name:
                return mock.internet.user_name()
            elif 'url' in column_name:
                return mock.internet.url()
            else:
                max_length = 100
                if hasattr(column.type, 'length') and column.type.length is not None:
                    max_length = column.type.length
                return ''.join(mock._random.choices(string.ascii_letters + string.digits, k=mock._random.randint(10, max_length)))
        
        elif 'date' in column_type:
            days = mock._random.randint(0, 5 * 365)
            date_value = datetime.date.today() - datetime.timedelta(days=days)
            
            if 'datetime' in column_type:
                time_value = datetime.time(
                    hour=mock._random.randint(0, 23),
                    minute=mock._random.randint(0, 59),
                    second=mock._random.randint(0, 59)
                )
                return datetime.datetime.combine(date_value, time_value)
            else:
                return date_value
        
        elif 'bool' in column_type:
            return mock._random.choice([True, False])
        
        return None

class SchemaUtils:
    """Helper class for schema-based integrations"""
    
    @staticmethod
    def from_json_schema(schema_definition, count=1, locale="en_US", seed=None):
        """Generate data from a JSON Schema"""
        try:
            import jsonschema
        except ImportError:
            raise ImportError("jsonschema is not installed. Install jsonschema to use this feature.")
        
        if isinstance(schema_definition, str):
            with open(schema_definition, 'r') as f:
                schema = json.load(f)
        else:
            schema = schema_definition
        
        mockpy_schema = SchemaUtils._convert_json_schema_to_mockpy_schema(schema)
        
        mock = MockPy(locale=locale, seed=seed)
        return mock.generate_dataset(mockpy_schema, count=count)
    
    @staticmethod
    def _convert_json_schema_to_mockpy_schema(json_schema):
        """Convert JSON Schema to MockPy schema"""
        result = {}
        
        if "properties" in json_schema:
            for prop_name, prop_schema in json_schema["properties"].items():
                result[prop_name] = SchemaUtils._convert_property_to_mockpy_field(prop_name, prop_schema)
        
        return result
    
    @staticmethod
    def _convert_property_to_mockpy_field(name, prop_schema):
        """Convert JSON Schema property to MockPy field definition"""
        if "type" not in prop_schema:
            return {"type": "lorem", "words": 5}
        
        schema_type = prop_schema["type"]
        
        if schema_type == "string":
            if "format" in prop_schema:
                format_type = prop_schema["format"]
                
                if format_type == "email":
                    return "person.email"
                elif format_type == "date":
                    return {"type": "date"}
                elif format_type == "date-time":
                    return {"type": "datetime"}
                elif format_type == "uri":
                    return "internet.url"
                elif format_type == "ipv4":
                    return "internet.ip_v4"
                elif format_type == "ipv6":
                    return "internet.ip_v6"
            
            if "name" in name.lower():
                if "first" in name.lower():
                    return "person.first_name"
                elif "last" in name.lower():
                    return "person.last_name"
                else:
                    return "person.full_name"
            elif "address" in name.lower():
                return "address.street_address"
            elif "city" in name.lower():
                return "address.city"
            elif "phone" in name.lower():
                return "person.phone_number"
            elif "company" in name.lower():
                return "company.company_name"
            elif "password" in name.lower():
                return "internet.password"
            elif "username" in name.lower():
                return "internet.user_name"
            elif "url" in name.lower():
                return "internet.url"
            elif "email" in name.lower():
                return "person.email"
            
            if "enum" in prop_schema:
                return {"type": "choice", "choices": prop_schema["enum"]}
            
            return {"type": "lorem", "words": 5}
        
        elif schema_type == "integer":
            min_val = prop_schema.get("minimum", 0)
            max_val = prop_schema.get("maximum", 100)
            
            return {"type": "integer", "min": min_val, "max": max_val}
        
        elif schema_type == "number":
            min_val = prop_schema.get("minimum", 0.0)
            max_val = prop_schema.get("maximum", 100.0)
            
            return {"type": "float", "min": min_val, "max": max_val, "precision": 2}
        
        elif schema_type == "boolean":
            return {"type": "choice", "choices": [True, False]}
        
        elif schema_type == "array":
            return []
        
        elif schema_type == "object":
            return SchemaUtils._convert_json_schema_to_mockpy_schema(prop_schema)
        
        return {"type": "lorem", "words": 5}

class FastAPIUtils:
    """Helper class for FastAPI integration"""
    
    @staticmethod
    def generate_pydantic_model(model_class, locale="en_US", seed=None, **field_overrides):
        """Generate an instance of a Pydantic model"""
        try:
            from pydantic import BaseModel
            if not issubclass(model_class, BaseModel):
                raise ValueError("model_class must be a Pydantic BaseModel class")
        except ImportError:
            raise ImportError("Pydantic is not installed. Install Pydantic to use this feature.")
        
        mock = MockPy(locale=locale, seed=seed)
        
        model_schema = model_class.schema()
        
        mockpy_schema = SchemaUtils._convert_json_schema_to_mockpy_schema(model_schema)
        
        data = mock.generate_dataset(mockpy_schema, count=1)[0]
        
        for field_name, value in field_overrides.items():
            data[field_name] = value
        
        return model_class(**data)

class integrations:
    """Module for integrations with different libraries and frameworks"""
    django = DjangoUtils
    flask = FlaskUtils
    sqlalchemy = SQLAlchemyUtils
    from_json_schema = SchemaUtils.from_json_schema
    fastapi = FastAPIUtils

if __name__ == "__main__":
    mock = MockPy(locale="tr_TR")
    
    person = mock.person.person()
    print(f"Person: {person.full_name}, Email: {person.email}, Birth Date: {person.birth_date}")
    
    address = mock.address.address()
    print(f"Address: {address.street}, {address.city}, {address.country}")
    
    company = mock.company.company()
    print(f"Company: {company.name}, Web: {company.website}")
    
    cc = mock.finance.credit_card()
    print(f"Card: {cc.formatted_number}, Expiration: {cc.expiration}, CVV: {cc.cvv}")
    
    schema = {
        "id": {"type": "integer", "min": 1000, "max": 9999},
        "user": "person.person",
        "subscription": {
            "plan": {"type": "choice", "choices": ["Basic", "Premium", "Enterprise"]},
            "start_date": {"type": "date", "start": "2022-01-01", "end": "2023-01-01"},
            "price": {"type": "float", "min": 9.99, "max": 99.99, "precision": 2},
            "is_active": {"type": "choice", "choices": [True, False]},
        },
        "billing": {
            "method": {"type": "choice", "choices": ["Credit Card", "Bank Transfer", "PayPal"]},
            "payment_info": "finance.credit_card"
        }
    }
    
    dataset = mock.generate_dataset(schema, count=2)
    
    print("\nGenerated Dataset:")
    for item in dataset:
        subscription = item.get("subscription", {})
        print(f"ID: {item.get('id')}")
        print(f"Plan: {subscription.get('plan')}")
        print(f"Start Date: {subscription.get('start_date')}")
        print(f"Price: {subscription.get('price')}")
        print(f"Status: {'Active' if subscription.get('is_active') else 'Inactive'}")
        print("---")