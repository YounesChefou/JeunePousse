const char[] = "123454321"

struct post_commands{
  const char *first_connexion = "first_connexion";
  const char *value = "value"; //envoyer les mesures
  const char *full_value = "full_value"; //envoyer les mesures + valeur des actionneurs
};
struct server_response{
  const char *correction = "correction"; //appliquer des valeurs sur les actionneurs
  const char *value = "value"; //demande d'envoie full_value
};
struct sensor{
  const char *Temperature = "Temperature";
  const char *Humidity = "Humidity";
  const char *GroundQuality = "GroundQuality";
  const char *WaterLevel = "WaterLevel";
  const char *Luminosity = "Luminosity";
};
struct action{
  const char *Temperature = "Temperature";
  const char *Humidity = "Humidity";
  const char *WaterLevel = "WaterLevel";
  const char *Luminosity = "Luminosity";
  const char *WaterFlow = "WaterFlow";
};
struct measure{
  float Temperature;
  float Humidity;
  float GroundQuality;
  float WaterLevel;
  float Luminosity;
}

/*
char *rand_string(size_t size){
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJK...";
    char *str = malloc(size + 1);
    if (size && str) {
        --size;
        for (size_t n = 0; n < size; n++) {
            int key = rand() % (int) (sizeof charset - 1);
            str[n] = charset[key];
        }
        str[size] = '\0';
    }
    return str;
}*/

void connect_to_server(){
  if (http.run() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_LINK);
    http.addHeader("Content-Type", "application/json");
  }
  sprintf(SERVER_LINK, "%s%d/%s", SERVER_URL, server_general_portCOM, p.first_connexion);
}
