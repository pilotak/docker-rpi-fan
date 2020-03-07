# Raspberry Pi variable speed cooling fan controller

Docker container that keeps the CPU temperature at desired level with PWM enabled fan based on [http://www.sensorsiot.org/variable-speed-cooling-fan-for-raspberry-pi-using-pwm-video138/](http://www.sensorsiot.org/variable-speed-cooling-fan-for-raspberry-pi-using-pwm-video138/)

## Docker-compose
```yaml
version: "3.7"
services:
  fan:
    container_name: fan
    restart: always
    image: pilotak/rpi-fan
    environment:
      - DESIRED_TEMP=45
      - FAN_PIN=12
      - FAN_PWM_MIN=25
      - FAN_PWM_MAX=100
      - FAN_PWM_FREQ=25
      - P_TEMP=15
      - I_TEMP=0.4
    devices:
      - /dev/gpiomem
```

### Environmental variables
Bellow are all available variables

| Variable | Description | Default value |
| --- | --- | :---:|
| `DESIRED_TEMP` | Temperature it tries to keep it at *(°C)* | 40 |
| `FAN_PIN` | PWM pin where is mosfet driver or load-switch connected to | 13 |
| `FAN_PWM_MIN` | Minimal duty cycle to turn the fan on *(%)* | 20 | 
| `FAN_PWM_MAX` | Maximal duty cycle of fan *(%)* | 100 | 
| `FAN_PWM_FREQ` | Broker address *(Hz)* | 17 | 
| `P_TEMP` | Proportional constant | 18.0 | 
| `I_TEMP` | Integral constant | 0.3 | 
| `READ_INTERVAL` | How often read the temperature *(seconds)* | 2 | 


