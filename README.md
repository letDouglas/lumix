
# Scontornamento delle immagini

Sviluppo di un servizio REST per lo scontornamento automatico di immagini di auto usate e integrazione in ambienti virtuali


Nell’ambito della vendita di auto usate, è fondamentale presentare le vetture in modo professionale e accattivante, spesso posizionandole su sfondi virtuali (es. saloni espositivi). Tuttavia, il processo manuale di:
Rimozione dello sfondo (scontornamento)
Gestione delle aree semitrasparenti (finestrini, luci, riflessi)
Integrazione realistica con nuovi sfondi
risulta lento, costoso e soggetto a errori.
Un’automazione di questo processo permetterebbe di:
Ridurre i tempi di elaborazione
Garantire risultati uniformi e professionali
Supportare grandi volumi di immagini
descrizione
Il progetto prevede lo sviluppo di un servizio REST in Spring Boot che:
Esegue lo scontornamento automatico delle immagini delle auto
Identifica le aree semitrasparenti (es. vetri) e le gestisce in modo da preservare il realismo.
Posiziona l’auto su un nuovo sfondo (es. salone virtuale) con corretta illuminazione e prospettiva.
Garantisce scalabilità e affidabilità tramite:
Spring Cloud (load balancing, fault tolerance) oppure
Kubernetes (containerizzazione, autoscaling)

## A che cosa serve il nostro servizio

Il progetto prevede lo sviluppo di un servizio REST in Spring Boot che:
Esegue lo scontornamento automatico delle immagini delle auto
Identifica le aree semitrasparenti (es. vetri) e le gestisce in modo da preservare il realismo.
Posiziona l’auto su un nuovo sfondo (es. salone virtuale) con corretta illuminazione e prospettiva.
Garantisce scalabilità e affidabilità tramite:
Spring Cloud (load balancing, fault tolerance) oppure
Kubernetes (containerizzazione, autoscaling)

## Linguaggi di programmazione usati

**Frontend** HTML

**Backend:** Aws, Express,Java,Python


## Note

Elaborazione immagini:
OpenCV
Pillow/Scikit-Image (Python, per post-processing)
Deep Learning (modelli preaddestrati per segmentation, es. U-Net)
REMBG https://github.com/danielgatis/rembg


## Attività

Analisi del problema e studio delle soluzioni esistenti
Valutazione di tool di background removal.
Definizione dei requisiti.
Progettazione dell’architettura
Scelta tra Spring Cloud o Kubernetes per l’affidabilità.
Design delle API REST (upload, processing, download).
Modello dati per tracciare le elaborazioni.
Implementazione del core di image processing
Integrazione di OpenCV/altre librerie per
Edge detection e rimozione dello sfondo.
Riconoscimento di aree trasparenti/semitrasparenti.
Ottimizzazione delle prestazioni (caching, batch processing).
Sviluppo del backend Spring
Creazione dei controller per l’upload e il processing.
Gestione degli errori e logging.
Deploy e ottimizzazione
Configurazione di Spring Cloud (Eureka, Hystrix) o
Containerizzazione con Docker e deploy su Kubernetes.
Test di carico e ottimizzazione delle performance.
Validazione e documentazione

## Deployment

To deploy this project run

```bash
  npm run deploy
```


## Run Locally

Clone the project

```bash
  git clone https://github.com/letDouglas/lumix.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```


## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    
