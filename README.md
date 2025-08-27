# EcoVolter Home Assistant Integrace

Integrace Home Assistant pro [nabíječky elektromobilů EcoVolter II](https://www.ecovolter.com/), která umožňuje lokálně ovládat základní funkce nabíjení, jako je zapínání a vypínání nabíjení, nastavení cílového proudu a sledování, zda je vaše vozidlo zapojeno do zásuvky nebo se aktivně nabíjí. Využívá jejich [API](https://asnplus.github.io/revc-charger-local-api-documentation/).

5% sleva na nabíječky https://www.nabijelektromobil.cz/ s kódem TYGRI nebo TYGRISK (pro nákup v EUR)

**Tato integrace podporuje pouze EcoVolter II (2. generace) s lokálním ovládáním.** Pokud máte 1. generaci s cloudovým API pomocí aplikace iXmanager, můžete použít [integraci iXmanager](https://github.com/kubacizek/home-assistant-ixmanager).

Je vyžadováno připojení k Wi-Fi. Pokud váš EcoVolter nemá povolenou Wi-Fi, můžete si jej odemknout za poplatek.

Tuto integraci původně vytvořil https://github.com/samuelg0rd0n/ha-ecovolter-integration

## Instalace

### Možnost 1: HACS (doporučeno)

1. Ujistěte se, že máte ve své instanci Home Assistant nainstalován [HACS](https://hacs.xyz/).
2. Přidejte tento repozitář jako vlastní repozitář v HACS:
- Přejděte do HACS → Nastavení → Repozitáře.
- Klikněte na tlačítko „+“.
- Přidejte repozitář: `rattkin/ha-ecovolter-integration`.
- Kategorie: Integrace.
3. Vyhledejte „EcoVolter“ v HACS → Integrace.
4. Klikněte na „Stáhnout“ a poté na „Restartovat Home Assistant“.
5. Přidejte integraci přes Nastavení → Zařízení a služby → Přidat integraci → Vyhledejte „EcoVolter“.

### Možnost 2: Ruční instalace

1. Stáhněte nebo naklonujte toto úložiště

2. Zkopírujte složku `custom_components/ecovolter` do adresáře `custom_components` vašeho Home Assistant

3. Restartujte Home Assistant

4. Přidejte integraci přes Nastavení → Zařízení a služby → Přidat integraci → Vyhledejte „EcoVolter“

## Konfigurace

1. V aplikaci Home Assistant přejděte do **Nastavení** → **Zařízení a služby**
2. Klikněte na **Přidat integraci**
3. Vyhledejte **"EcoVolter"** a vyberte ho
4. Zadejte sériové číslo vaší nabíječky EcoVolter. Toto číslo najdete v aplikaci EV-Manager (aplikace pro iOS/Android) nebo je vytištěno přímo na nabíječce.

5. Zadejte tajný klíč vaší nabíječky. Ve výchozím nastavení je totožný s vaším sériovým číslem. EcoVolter uvádí, že od srpna 2025 bude v nadcházejících verzích aplikace EV-Manager přidána možnost nastavení tajného klíče.

6. Klikněte na **Odeslat**

## Funkce

### Binární senzory
- **Nabíjí se**: Zobrazuje, zda nabíječka aktivně nabíjí vaše vozidlo
- **Je vozidlo připojeno**: Zobrazuje, zda je vozidlo připojeno k nabíječce
- **3fázový režim povolen**: Zobrazuje aktuální stav fázového režimu

### Senzory
- **Skutečný výkon**: Spotřeba energie v reálném čase ve wattech

### Ovládání
- **Spuštění/zastavení nabíjení**: Ovládání nabíjecích relací
- **Nastavení cílového proudu**: Úprava nabíjecího proudu (6 A až 16 A)
- **Řízení 3fázového režimu**: Povolení nebo zakázání 3fázového režimu nabíjení

## Požadavky

- Home Assistant 2023.8.0 nebo novější
- Nabíječka pro elektromobily EcoVolter II (2. generace) s připojením k síti
- Podpora mDNS ve vašem nastavení

## Řešení problémů

- **Integrace nenalezena**: Ujistěte se, že jste po instalaci restartovali Home Assistant
- **Připojení selhalo**: Ověřte sériové číslo a připojení k síti vaší nabíječky
- **Chyba ověřování**: Zkontrolujte tajný klíč vaší nabíječky

## Podpora

Pokud narazíte na nějaké problémy nebo máte dotazy, prosím:
1. Zkontrolujte výše uvedenou část pro řešení problémů
2. Zkontrolujte protokoly Home Assistant, zda neobsahují chybové zprávy
3. Otevřete v tomto repozitáři zprávu o problému s podrobnými informacemi o vašem nastavení