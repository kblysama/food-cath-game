import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
GENISLIK = 800
YUKSEKLIK = 600

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
KIRMIZI = (255, 0, 0)
YESIL = (34, 139, 34)

# Ekranı oluştur
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yemek Toplama Oyunu")

# Arka plan ve emoji görsellerini yükle
arkaplan = pygame.image.load("assets/mutfak.png")
arkaplan = pygame.transform.scale(arkaplan, (GENISLIK, YUKSEKLIK))
sinirli_emoji = pygame.image.load("assets/sinirli.png")
sinirli_emoji = pygame.transform.scale(sinirli_emoji, (80, 80))  # Karakterden biraz küçük
tabak_emoji = pygame.image.load("assets/tabak.png")
tabak_emoji = pygame.transform.scale(tabak_emoji, (80, 80))  # Sinirli emoji ile aynı boyut

# Font ayarları
font = pygame.font.Font(None, 36)
buyuk_font = pygame.font.Font(None, 48)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface):
        color = (self.color[0]-30, self.color[1]-30, self.color[2]-30) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, SIYAH, self.rect, 2, border_radius=12)
        
        text_surface = font.render(self.text, True, SIYAH)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

def giris_ekrani():
    basla_button = Button(GENISLIK//2 - 100, YUKSEKLIK//2 + 50, 200, 50, "BAŞLA", YESIL)
    
    while True:
        ekran.blit(arkaplan, (0, 0))
        
        # Başlık
        baslik_text = buyuk_font.render("SUDE'Yİ DOYURMAK İÇİN BAŞLA!", True, KIRMIZI)
        baslik_rect = baslik_text.get_rect(center=(GENISLIK//2, YUKSEKLIK//2 - 50))
        ekran.blit(baslik_text, baslik_rect)
        
        # Alt yazı
        altyazi_text = font.render("SUDE BUGÜN HİÇBİR ŞEY YEMEDİ VE ÇOK SİNİRLİ!", True, SIYAH)
        altyazi_rect = altyazi_text.get_rect(center=(GENISLIK//2, YUKSEKLIK//2))
        ekran.blit(altyazi_text, altyazi_rect)
        
        # Butonu çiz
        basla_button.draw(ekran)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if basla_button.handle_event(event):
                return  # Oyunu başlat
        
        pygame.display.flip()
        clock.tick(60)

# Karakter sınıfı
class Karakter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/karakter.png")
        self.image = pygame.transform.scale(self.image, (80, 120))
        self.rect = self.image.get_rect()
        self.rect.x = GENISLIK // 2
        self.rect.y = YUKSEKLIK - 120
        self.hiz = 7

    def hareket(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.hiz
        if keys[pygame.K_RIGHT] and self.rect.right < GENISLIK:
            self.rect.x += self.hiz

# Yemek sınıfı
class Yemek(pygame.sprite.Sprite):
    def __init__(self, resim_adi):
        super().__init__()
        self.image = pygame.image.load(f"assets/{resim_adi}")
        # Yoğurt için özel boyut
        if resim_adi == "yogurt.png":
            self.image = pygame.transform.scale(self.image, (80, 80))  # Yoğurt daha büyük
        else:
            self.image = pygame.transform.scale(self.image, (50, 50))  # Diğer yemekler normal boyut
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - self.rect.width)
        self.rect.y = -50
        self.hiz = random.randint(3, 7)
        self.tip = resim_adi
        # Yemek tipine göre puan belirleme
        if resim_adi == "manti.png":
            self.puan = 10
        elif resim_adi == "patates.png":
            self.puan = 5
        elif resim_adi == "tavuk.png":
            self.puan = 20
        elif resim_adi == "yogurt.png":
            self.puan = 10
        elif resim_adi == "pirasa.png":
            self.puan = -10
        else:  # bamya.png
            self.puan = -20

    def update(self):
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            return True
        return False

# Sprite grupları
karakter_grup = pygame.sprite.Group()
yemek_grup = pygame.sprite.Group()

# Karakteri oluştur
karakter = Karakter()
karakter_grup.add(karakter)

# FPS için clock nesnesi
clock = pygame.time.Clock()

# Yemek oluşturma zamanlayıcısı
YEMEK_OLUSTUR = pygame.USEREVENT + 1
pygame.time.set_timer(YEMEK_OLUSTUR, 2000)  # Her 2 saniyede bir

def oyun_bitti_ekrani():
    ekran.blit(arkaplan, (0, 0))  # Arka planı çiz
    game_over_text = font.render("SUDE'Yİ DOYURAMADIN BUNUN SONUÇLARINA KATLANACAKSIN!!", True, KIRMIZI)
    skor_text = font.render(f"Toplam Puan: {puan}", True, SIYAH)
    tekrar_text = font.render("Tekrar oynamak için SPACE'e basın", True, SIYAH)
    
    game_over_rect = game_over_text.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 - 50))
    skor_rect = skor_text.get_rect(center=(GENISLIK/2, YUKSEKLIK/2))
    tekrar_rect = tekrar_text.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 + 50))
    
    ekran.blit(game_over_text, game_over_rect)
    ekran.blit(skor_text, skor_rect)
    ekran.blit(tekrar_text, tekrar_rect)
    pygame.display.flip()
    
    bekle = True
    while bekle:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
    return False

def oyunu_sifirla():
    global puan, can
    puan = 0
    can = 100
    yemek_grup.empty()

def oyun_dongusu():
    global puan, can
    
    # Emoji gösterimi için zamanlayıcı
    emoji_goster = False
    emoji_zamanlayici = 0
    emoji_tip = None  # "sinirli" veya "tabak"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == YEMEK_OLUSTUR:
                yemek_tipi = random.choice(["manti.png", "patates.png", "bamya.png", 
                                          "tavuk.png", "yogurt.png", "pirasa.png"])
                yemek = Yemek(yemek_tipi)
                yemek_grup.add(yemek)
        
        # Karakter hareketi
        karakter.hareket()
        
        # Yemekleri güncelle ve kaçanları kontrol et
        for yemek in yemek_grup.sprites():
            if yemek.update():  # Eğer yemek ekrandan çıktıysa
                if yemek.tip not in ["bamya.png", "pirasa.png"]:  # İyi yemekleri kaçırınca can kaybet
                    can -= 10
                    # Emoji gösterimini başlat
                    emoji_goster = True
                    emoji_zamanlayici = pygame.time.get_ticks()
                    emoji_tip = "sinirli"
                yemek_grup.remove(yemek)
                
                if can <= 0:
                    if oyun_bitti_ekrani():
                        oyunu_sifirla()
                    else:
                        return
        
        # Çarpışma kontrolü
        carpismalar = pygame.sprite.spritecollide(karakter, yemek_grup, True)
        for carpisan in carpismalar:
            puan += carpisan.puan
            # Emoji gösterimini ayarla
            emoji_goster = True
            emoji_zamanlayici = pygame.time.get_ticks()
            
            if carpisan.tip in ["bamya.png", "pirasa.png"]:
                # Negatif puanlı yemekler için sinirli emoji ve uyarı
                emoji_tip = "sinirli"
                # Bamya ve pırasa için farklı can kaybı
                if carpisan.tip == "bamya.png":
                    can -= 25
                else:  # pirasa.png
                    can -= 15
                uyari_text = font.render(f"{carpisan.puan} Puan! {carpisan.tip.split('.')[0].capitalize()} yakaladın!", True, KIRMIZI)
                ekran.blit(uyari_text, (GENISLIK//2 - 150, 100))
                pygame.display.flip()
                pygame.time.wait(500)
            else:
                # Pozitif puanlı yemekler için tabak emoji
                emoji_tip = "tabak"
            
            if can <= 0:  # Can kontrolü
                if oyun_bitti_ekrani():
                    oyunu_sifirla()
                else:
                    return
        
        # Ekranı temizle ve arka planı çiz
        ekran.blit(arkaplan, (0, 0))
        
        # Can barını çiz
        can_genislik = 200
        can_yukseklik = 20
        can_x = GENISLIK - can_genislik - 10
        can_y = 20  # Y pozisyonunu biraz aşağı aldım
        
        # Can barı arka planı (kırmızı)
        pygame.draw.rect(ekran, KIRMIZI, (can_x, can_y, can_genislik, can_yukseklik))
        # Mevcut can (yeşil)
        mevcut_can_genislik = (can / 100) * can_genislik
        if mevcut_can_genislik > 0:
            pygame.draw.rect(ekran, YESIL, (can_x, can_y, mevcut_can_genislik, can_yukseklik))
        # Can barı çerçevesi
        pygame.draw.rect(ekran, SIYAH, (can_x, can_y, can_genislik, can_yukseklik), 2)
        
        # Can miktarını yaz
        can_text = font.render(f"HP: {max(0, can)}", True, SIYAH)
        ekran.blit(can_text, (can_x - 100, can_y - 5))  # X pozisyonunu daha sola aldım
        
        # Puanı göster
        puan_text = font.render(f"Puan: {puan}", True, SIYAH)
        ekran.blit(puan_text, (10, 10))
        
        # Sprite'ları çiz
        karakter_grup.draw(ekran)
        yemek_grup.draw(ekran)
        
        # Emoji gösterimi
        if emoji_goster:
            # Emoji pozisyonu (karakterin sağ üstü)
            emoji_x = karakter.rect.right - 20
            emoji_y = karakter.rect.top - 40
            
            # Emoji tipine göre göster
            if emoji_tip == "sinirli":
                ekran.blit(sinirli_emoji, (emoji_x, emoji_y))
            elif emoji_tip == "tabak":
                ekran.blit(tabak_emoji, (emoji_x, emoji_y))
            
            # 1 saniye sonra emojiyi kaldır
            if pygame.time.get_ticks() - emoji_zamanlayici > 1000:
                emoji_goster = False
        
        # Ekranı güncelle
        pygame.display.flip()
        
        # FPS'i 60 olarak ayarla
        clock.tick(60)

if __name__ == "__main__":
    puan = 0
    can = 100  # Başlangıç canı
    giris_ekrani()  # Önce giriş ekranını göster
    oyun_dongusu()  # Sonra oyunu başlat 