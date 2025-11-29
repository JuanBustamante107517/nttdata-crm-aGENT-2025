# Simulación de base de datos de redes sociales (Mock)
def obtener_redes_sociales(cliente_id):
    # Base de datos ficticia
    mock_db = {
        1: {
            "red": "Twitter/X", 
            "intereses": ["Inteligencia Artificial", "Startups", "Gaming"],
            "ultimo_post": "Increíble lo nuevo de OpenAI #Tech",
            "nivel_actividad": "Alto"
        },
        2: {
            "red": "Instagram", 
            "intereses": ["Wellness", "Recetas Saludables", "Mindfulness"],
            "ultimo_post": "Foto de batido verde en la playa 🌴",
            "nivel_actividad": "Medio"
        },
        3: {
            "red": "LinkedIn", 
            "intereses": ["SaaS", "Transformación Digital", "Networking"],
            "ultimo_post": "Buscando proveedores de nube híbrida.",
            "nivel_actividad": "Muy Alto"
        },
        4: {
            "red": "Facebook", 
            "intereses": ["Noticias Economía", "Golf", "Vinos"],
            "ultimo_post": "Compartió una noticia sobre la bolsa de valores.",
            "nivel_actividad": "Bajo"
        },
        5: {
            "red": "TikTok", 
            "intereses": ["Trends de baile", "Study hacks", "Moda low-cost"],
            "ultimo_post": "Video de unboxing de papelería.",
            "nivel_actividad": "Alto"
        }
    }
    
    # Retornar datos o un default si no existe
    return mock_db.get(cliente_id, {"red": "N/A", "intereses": ["General"], "ultimo_post": "Sin actividad reciente"})