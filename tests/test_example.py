from app.controllers.exemplo_controller import ExemploController

def test_exemplo_controller() -> None:
    controller = ExemploController()
    response = controller.handle_request()
    assert response == "Dados: Olá, MVC!"
