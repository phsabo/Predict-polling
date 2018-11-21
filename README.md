# Predict polling

## Predict Polling System to Medium access control (MAC)

### Paulo Henrique Sabo UTFPR-CM/UNICAMP

- Protocolo de acesso ao meio (MAC) sem fio baseado em técnica de polling.

Simples e de pouca necessidade de hardware, não necessita de sincronismo (schedule) e a prova de colisões. Este protocolo de acesso ao meio garante pouco tempo de uso do rádio, em comparação com CSMA/CA, provendo grande economia de energia. De grande utilidade em dispositivos alimentados por bateria.

- Nó utilizado para implementação:
https://github.com/phsabo/NodePHS/wiki

- Necessário a biblioteca https://github.com/nRF24/RF24 para integração com o módulo de rádio nRF24l01+

- Implementação de polling tradicional Round-Robin para Arduino e Raspberry Pi.
--  Para módulo nRF24l01+

- Implementação de Predict polling para Raspberry Pi
--  Para módulo nRF24l01+
