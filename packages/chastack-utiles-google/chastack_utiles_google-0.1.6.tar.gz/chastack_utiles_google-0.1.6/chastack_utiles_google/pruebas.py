import unittest
from unittest.mock import patch, MagicMock
from chastack_utiles_google.recurso import Recurso, TipoServicioGoogleApi
from chastack_utiles_google.correo import Correo, CorreoHTML, gMail
from chastack_utiles_google.hojas_de_calculo import gSheets, HojaDeCalculo

class TestGoogleApis(unittest.TestCase):
    def setUp(self):
        self.mock_google_service = MagicMock()
        self.mock_google_service.spreadsheets().values().get.return_value.execute.return_value = {'values': [['A1', 'B1'], ['A2', 'B2']]}
        self.mock_google_service.spreadsheets().values().update.return_value.execute.return_value = {'updatedCells': 4}
        self.patcher = patch('chastack_utiles_google.recurso.construirRecurso', return_value=self.mock_google_service)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_recurso_init_valid(self):
        credenciales = {"type": "service_account", "project_id": "test"}
        recurso = Recurso(credenciales, TipoServicioGoogleApi.SHEETS)
        self.assertIsNotNone(recurso)

    def test_correo_creacion(self):
        correo = Correo.crear("test@example.com", "dest@example.com", "Asunto", "Cuerpo")
        self.assertIsNotNone(correo)
        self.assertIn("Asunto", correo.mensajeCodificado()["raw"])

    def test_correo_anadir_adjunto(self):
        correo = Correo.crear("test@example.com", "dest@example.com", "Asunto", "Cuerpo")
        with patch("builtins.open", new_callable=MagicMock):
            correo.anadirAdjunto("test.txt")
        self.assertIsNotNone(correo)

    def test_gmail_envio(self):
        credenciales = {"type": "service_account", "project_id": "test"}
        gmail = gMail(credenciales, "test@example.com")
        correo = Correo.crear("test@example.com", "dest@example.com", "Asunto", "Cuerpo")
        with patch.object(gmail._Recurso__recursoSubyacente.users().messages(), "send", return_value=MagicMock(execute=MagicMock(return_value={"id": "1234"}))):
            result = gmail.enviarCorreo(correo)
        self.assertEqual(result["id"], "1234")

    def test_hoja_creacion(self):
        credenciales = {"type": "service_account", "project_id": "test"}
        sheets = gSheets(credenciales, "test@example.com")
        with patch.object(sheets._Recurso__recursoSubyacente.spreadsheets(), "create", return_value=MagicMock(execute=MagicMock(return_value={"spreadsheetId": "abcd1234"}))):
            hoja = sheets.crear("Test Sheet")
        self.assertEqual(hoja.id, "abcd1234")

    def test_hoja_escribir(self):
        credenciales = {"type": "service_account", "project_id": "test"}
        sheets = gSheets(credenciales, "test@example.com")
        with patch.object(sheets._Recurso__recursoSubyacente.spreadsheets().values(), "update", return_value=MagicMock(execute=MagicMock(return_value={"updatedCells": 4}))):
            result = sheets.escribir("abcd1234", "A1:B2", [[1, 2], [3, 4]])
        self.assertEqual(result["updatedCells"], 4)

if __name__ == '__main__':
    unittest.main()
