# ComPuter - Sistema de Recomendación de Componentes de PC

ComPuter es una aplicación web inteligente que ayuda a los usuarios a seleccionar los mejores componentes para armar su PC ideal. Utiliza inteligencia artificial para proporcionar recomendaciones personalizadas basadas en el presupuesto, tipo de uso y preferencias del usuario.

## 🚀 Características Principales

### 🤖 Asistente Virtual (Chatbot)
- **Procesamiento de Lenguaje Natural (NLP)**: Comprende consultas en español sobre componentes de PC
- **Detección de Intenciones**: Identifica automáticamente qué tipo de ayuda necesita el usuario
- **Recomendaciones Inteligentes**: Integrado con el motor de IA para sugerencias personalizadas
- **Historial de Conversación**: Mantiene el contexto de la conversación para mejores respuestas

### 🧠 Motor de Recomendación IA
- **Algoritmos de Machine Learning**: Utiliza scikit-learn para análisis y recomendaciones
- **Distribución Inteligente de Presupuesto**: Optimiza la asignación de recursos según el tipo de uso
- **Análisis de Compatibilidad**: Verifica automáticamente la compatibilidad entre componentes
- **Puntuación de Rendimiento**: Evalúa y compara el rendimiento de diferentes configuraciones

### 🔐 Sistema de Autenticación
- **JWT (JSON Web Tokens)**: Autenticación segura y sin estado
- **Gestión de Usuarios**: Registro, login y perfiles de usuario
- **Sesiones Persistentes**: Mantiene las preferencias y historial del usuario

### 🎨 Interfaz de Usuario Moderna
- **React + TypeScript**: Frontend moderno y tipado
- **Material-UI**: Componentes elegantes y responsivos
- **Diseño Responsivo**: Optimizado para desktop y móvil
- **Comparación Lado a Lado**: Herramienta visual para comparar componentes

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos relacional robusta
- **Scikit-learn**: Biblioteca de machine learning
- **NLTK/TextBlob**: Procesamiento de lenguaje natural
- **Pydantic**: Validación de datos y serialización

### Frontend
- **React 18**: Biblioteca de interfaz de usuario
- **TypeScript**: Superset tipado de JavaScript
- **Material-UI (MUI)**: Componentes de interfaz
- **Axios**: Cliente HTTP para comunicación con la API
- **React Router**: Navegación del lado del cliente

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior (recomendado 3.9-3.10)
- **Node.js**: 16 o superior
- **PostgreSQL**: 12 o superior
- **npm/yarn**: Para gestión de paquetes del frontend

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd ComPuter
```

### 2. Configurar el Backend

#### Crear entorno virtual
```bash
cd backend
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

#### Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Configurar base de datos
1. Crear una base de datos PostgreSQL llamada `computer_db`
2. Crear archivo `.env` en el directorio `backend`:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost/computer_db
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Inicializar base de datos
```bash
# Crear tablas y poblar con datos de muestra
python populate_db.py
```

#### Entrenar modelo NLP
```bash
# Entrenar el modelo de procesamiento de lenguaje natural
python train_nlp.py
```

### 3. Configurar el Frontend

```bash
cd frontend
npm install
```

### 4. Ejecutar la Aplicación

#### Iniciar el backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Iniciar el frontend
```bash
cd frontend
npm start
```

La aplicación estará disponible en:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📖 Uso de la Aplicación

### 1. Registro y Autenticación
- Crear una cuenta nueva o iniciar sesión
- El sistema mantendrá tus preferencias y historial

### 2. Chatbot Inteligente
- Haz clic en el ícono del chatbot (esquina inferior derecha)
- Pregunta sobre componentes: "¿Qué procesador me recomiendas?"
- Solicita recomendaciones: "Necesito una PC para gaming con $1000"
- Consulta compatibilidad: "¿Es compatible este CPU con esta placa?"

### 3. Explorar Componentes
- Navega por las categorías de componentes
- Usa los filtros para encontrar productos específicos
- Compara componentes lado a lado

### 4. Obtener Recomendaciones
- Especifica tu presupuesto y tipo de uso
- El sistema generará una configuración optimizada
- Revisa las explicaciones de cada recomendación

## 🤖 Capacidades del Chatbot

El asistente virtual puede ayudarte con:

### Tipos de Consultas Soportadas
- **Recomendaciones**: "Recomiéndame una PC para gaming"
- **Información de Componentes**: "¿Qué es mejor, SSD o HDD?"
- **Compatibilidad**: "¿Funciona esta RAM con mi motherboard?"
- **Presupuesto**: "¿Qué puedo comprar con $800?"
- **Tipo de Uso**: "Componentes para edición de video"
- **Comparaciones**: "Compara estos dos procesadores"

### Ejemplos de Preguntas
```
- "Necesito una PC para gaming con presupuesto de $1200"
- "¿Qué diferencia hay entre DDR4 y DDR5?"
- "¿Cuánta RAM necesito para programación?"
- "Recomiéndame una tarjeta gráfica para 1440p"
- "¿Es compatible el Ryzen 5 5600X con la placa B550?"
```

## 🔧 Estructura del Proyecto

```
ComPuter/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── auth.py
│   │   │       ├── components.py
│   │   │       ├── recommendations.py
│   │   │       └── chatbot.py
│   │   ├── models/
│   │   ├── ai_engine.py
│   │   ├── chatbot.py
│   │   ├── nlp_training.py
│   │   ├── sample_data.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── train_nlp.py
│   └── populate_db.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBot/
│   │   │   ├── ComponentList/
│   │   │   └── Recommendations/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 🚀 Despliegue

### Producción con Docker (Próximamente)
```bash
docker-compose up -d
```

### Variables de Entorno para Producción
```env
DATABASE_URL=postgresql://user:pass@db:5432/computer_db
SECRET_KEY=production_secret_key
DEBUG=False
CORS_ORIGINS=["https://tu-dominio.com"]
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la documentación de la API en `/docs`
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que la base de datos esté configurada correctamente
4. Verifica que el modelo NLP esté entrenado

## 🔮 Próximas Características

- [ ] Integración con APIs de tiendas en línea
- [ ] Comparador de precios en tiempo real
- [ ] Notificaciones de ofertas y descuentos
- [ ] Calculadora de rendimiento en juegos
- [ ] Soporte para múltiples idiomas
- [ ] Aplicación móvil nativa
- [ ] Sistema de reviews y calificaciones

---

**ComPuter** - Tu asistente inteligente para armar la PC perfecta 🖥️✨inteligencia artificial.

## Descripción

ComPuter es una plataforma que ayuda a los usuarios a seleccionar componentes de PC compatibles entre sí y optimizados para sus necesidades específicas, utilizando un sistema de recomendación basado en IA. Funciona como un mostrador virtual de componentes (CPU, GPU, RAM, etc.) con información detallada sobre especificaciones, generaciones y precios actualizados.

## Fundamentación

El mercado de componentes computacionales es amplio y técnico, lo que genera una barrera de entrada para usuarios no expertos. Este proyecto aborda la necesidad de asesoramiento inteligente y personalizado, considerando:

- Compatibilidad entre componentes
- Precios actualizados
- Perfil de uso del usuario (diseñador gráfico, programador, arquitecto, etc.)

Ofrece un valor diferenciado al integrar en una sola plataforma:
- Comparativas detalladas
- Recomendaciones basadas en IA
- Orientación según presupuesto y necesidades específicas

## Objetivos

### Objetivo General

Desarrollar un sistema web de recomendación y comparativa de componentes computacionales que integre un asistente de IA para sugerir configuraciones compatibles y optimizadas según presupuesto y perfil de usuario, proporcionando una herramienta de apoyo a la decisión de compra.

### Objetivos Específicos

1. Diseñar e implementar una base de datos que almacene componentes, especificaciones, precios y reglas de compatibilidad
2. Implementar un módulo de IA con algoritmos de recomendación basados en perfil y presupuesto
3. Desarrollar una interfaz web responsive para buscar, visualizar y comparar componentes
4. Integrar un asistente virtual (chatbot) con capacidades de NLP
5. Implementar un módulo de comparativa side-by-side con análisis de viabilidad
6. Desarrollar un panel de administración para gestionar componentes, precios y usuarios
7. Realizar pruebas de funcionalidad, usabilidad y rendimiento
8. Documentar el proceso de desarrollo y los manuales de usuario

## Estructura del Proyecto

El proyecto está dividido en dos partes principales:

- **Backend**: API desarrollada con FastAPI y PostgreSQL
- **Frontend**: Aplicación web desarrollada con React y TypeScript

## Fases de Desarrollo

1. **Entorno & Planificación**: Configuración de repositorios y herramientas de gestión
2. **Base de Datos & Backend**: Desarrollo de la API y modelado de datos
3. **Motor de IA & Recomendaciones**: Implementación de algoritmos de recomendación
4. **Frontend & Panel de Admin**: Desarrollo de la interfaz de usuario
5. **Integración & Pruebas**: Testing y refinamiento
6. **Despliegue & Lanzamiento**: Publicación de la aplicación

## Tecnologías

- **Backend**: Python, FastAPI, PostgreSQL, SQLAlchemy
- **Frontend**: React, TypeScript, Material-UI
- **IA**: Scikit-learn, Pandas, NumPy, Rasa
- **DevOps**: Docker, GitHub Actions

## Funcionalidades Implementadas

- **Motor de Recomendación IA**: Genera recomendaciones personalizadas basadas en presupuesto y preferencias
- **Verificación de Compatibilidad**: Asegura que los componentes seleccionados sean compatibles entre sí
- **Perfiles de Usuario**: Guarda preferencias y configuraciones para recomendaciones futuras
- **Panel de Administración**: Gestión de componentes y usuarios para administradores
- **Autenticación Segura**: Sistema de autenticación JWT con contraseñas encriptadas