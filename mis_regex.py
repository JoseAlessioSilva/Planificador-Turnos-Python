class MisRegex():

    def regex_nombre(self, ):
        """
        Esta función devuelve el patrón regex para validar nombres.
        El patrón permite letras mayúsculas y minúsculas, incluyendo vocales acentuadas
        """
        patron = "^[A-Za-záéíóú]*$"
        return patron
