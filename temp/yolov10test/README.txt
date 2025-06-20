YOLOV10

Base del microservizio che deve riceve come input una immagine ritaglia e restituisce l'area precisa di tutti i vetri utilizzando yolov10, in modo che poi questi possano essere resi trasparenti da un altro microservizio.

Problemi:
- Sta usando yolov8 e non yolov10 perchè yolov10 può solo trovare i vetri e evidenziarli con rettangoli, non può trovare la zona precisa
- Non ci sono modelli gia pronti allenati per trovare i vetri delle macchine
- Non ci sta modo di allenare un modello e scaricarne i pesi per fare funzionare bene il servizio come vogliamo (roboflow non può essere utilizzato)

Il programma attuale è stato fatto per vedere il funzionamento di yolo e come fare andare la repo python, che sarà poi fatto andare da un backend java come BlenderApp usando Processbuilder
