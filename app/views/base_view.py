from flask import jsonify
from app.utils.types.views.base_view.viewReturn import ViewReturn
from app.utils.types.views.base_view.viewParams import ViewParams

class BaseView:
    @staticmethod
    def render(params: ViewParams):
        """
        Renders a standardized JSON response for the API.
        
        Args:
            params (ViewParams): The parameters for the response (data, status, message).

        Returns:
            Response: A Flask Response object containing the JSON response.
        """
        response_data = ViewReturn(status=params.status, message=params.message, data=params.data)
        return jsonify(response_data.__dict__), params.status
