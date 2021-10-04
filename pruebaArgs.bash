python3 FWQ_Engine.py 192.168.1.10:5555 100 192.168.1.10:5555
python3 FWQ_WaitingTimeServer.py 5555 1.1.1.1:5555
python3 FWQ_Visitor.py 192.168.1.10:5555 1.1.1.1:5555
python3 FWQ_Sensor.py 192.168.1.10:5555 5555
python3 FWQ_Registry.py 5555
echo "-------------ERRORES ESPERADOS DE IP -----------------------"
python3 FWQ_Engine.py 192168.1.10:5555 100 192.168.1.10:5555
python3 FWQ_WaitingTimeServer.py 5555 11.1.1:5555
python3 FWQ_Visitor.py 192168.1.10:5555 11.1.1:5555
python3 FWQ_Sensor.py 192168.1.10:5555 5555
python3 FWQ_Registry.py 5555
echo "-------------ERRORES ESPERADOS DE PUERTO -----------------------"
python3 FWQ_Engine.py 192.168.1.10;5555 100 192.168.1.10;5555
python3 FWQ_WaitingTimeServer.py 5555 1.1.1.1;5555
python3 FWQ_Visitor.py 192.168.1.10;5555 1.1.1.1;5555
python3 FWQ_Sensor.py 192.168.1.10;5555 5555
python3 FWQ_Registry.py 5555