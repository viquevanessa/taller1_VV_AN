
String pot1;
String pot2;
String conca;

void setup() {
  
  Serial.begin(9600);
}
void loop() {

  pot1 = String(analogRead(A0),DEC);
  pot2 = String(analogRead(A1),DEC);
  conca = pot1 +','+pot2;
  
  
  Serial.println(conca);
  delay(500);

}
