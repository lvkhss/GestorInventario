# 📦 GestorInventario

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**Sistema de Gestión de Inventario Completo para Empresas Chilenas**

[🚀 Demo](#demo) • [📥 Instalación](#instalación) • [📖 Documentación](#documentación) • [🤝 Contribuir](#contribuir)

</div>

---

## 🌟 Características Principales

<table>
<tr>
<td width="50%">

### 🏪 **Gestión de Inventario**
- ✅ Productos con tipos dinámicos
- ✅ Control de stock en tiempo real
- ✅ Códigos de barras opcionales
- ✅ Historial completo de movimientos
- ✅ Carga masiva vía Excel

### 🛒 **Sistema de Ventas**
- ✅ Carrito interactivo con animaciones
- ✅ Códigos de boleta secuenciales chilenos
- ✅ Recibos estilo boleta tradicional
- ✅ Tracking completo de transacciones

</td>
<td width="50%">

### 👥 **Gestión de Usuarios**
- ✅ Sistema de roles (Staff/Usuario)
- ✅ Validación RUT chileno
- ✅ Perfiles con estadísticas personalizadas
- ✅ Control de permisos granular

### 🏢 **Proveedores**
- ✅ Base de datos de proveedores
- ✅ Información de contacto completa
- ✅ Validación de datos empresariales

</td>
</tr>
</table>

---

## 🖼️ Capturas de Pantalla

<div align="center">

### Dashboard Principal
<img src="https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard+Principal" alt="Dashboard" width="70%">

### Sistema de Carrito
<img src="https://via.placeholder.com/400x300/764ba2/ffffff?text=Carrito+Interactivo" alt="Carrito" width="35%"> <img src="https://via.placeholder.com/400x300/2f855a/ffffff?text=Recibo+de+Venta" alt="Recibo" width="35%">

</div>

---

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.7+
- pip
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/GestorInventario.git
cd GestorInventario
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```

¡Visita `http://127.0.0.1:8000` y comienza a usar el sistema! 🎉

---

## 🛠️ Stack Tecnológico

<div align="center">

| Frontend | Backend | Base de Datos | Otros |
|----------|---------|---------------|-------|
| Bootstrap 5.3 | Django 5.2.1 | SQLite3 | WhiteNoise |
| JavaScript Vanilla | Python 3.7+ | PostgreSQL (prod) | django-import-export |
| CSS3 Custom | Django ORM | | pandas, openpyxl |
| SVG Icons | Django Templates | | django-humanize |

</div>

---

## 📋 Funcionalidades Específicas para Chile

### 🇨🇱 **Adaptado al Mercado Chileno**
- **Validación RUT**: Algoritmo completo de validación de RUT personas y empresas
- **Códigos de Boleta**: Sistema secuencial BOL-00000001, BOL-00000002...
- **Moneda Chilena**: Precios en pesos chilenos sin decimales
- **Formato de Fechas**: DD/MM/YYYY según estándar chileno

---

## 📖 Estructura del Proyecto

```
GestorInventario/
├── 📁 inventory/                    # App principal
│   ├── 📁 static/                   # CSS, JS, imágenes
│   ├── 📁 templates/                # Plantillas HTML
│   ├── 📁 templatetags/             # Filtros personalizados
│   ├── 📄 models.py                 # 6 modelos principales
│   ├── 📄 views.py                  # 30+ vistas (937 líneas)
│   ├── 📄 forms.py                  # 8 formularios con validaciones
│   └── 📄 urls.py                   # 20+ endpoints
├── 📁 inventory_management_system/  # Configuración Django
├── 📄 db.sqlite3                   # Base de datos
├── 📄 requirements.txt             # Dependencias
├── 📄 productos.xlsx               # Archivo ejemplo
└── 📄 Dockerfile                   # Configuración Docker
```

---

## 🎯 Casos de Uso

<table>
<tr>
<td width="33%">

### 🏪 **Pequeños Comercios**
- Control de stock básico
- Ventas rápidas
- Proveedores principales
- Reportes semanales

</td>
<td width="33%">

### 🏭 **Talleres y Fábricas**
- Inventario de materiales
- Control de consumo
- Movimientos por usuario
- Tipos de productos dinámicos

</td>
<td width="33%">

### 🏢 **Oficinas y Servicios**
- Suministros de oficina
- Equipos y herramientas
- Control de activos
- Múltiples usuarios

</td>
</tr>
</table>

---

## 🔧 Configuración Avanzada

### Variables de Entorno (Producción)
```bash
DEBUG=False
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

### Docker
```bash
docker build -t gestor-inventario .
docker run -p 8000:8000 gestor-inventario
```

---

## 📊 Estadísticas del Proyecto

<div align="center">

| Métrica | Valor |
|---------|-------|
| **Líneas de Código** | ~3,000+ |
| **Plantillas HTML** | 20+ |
| **Modelos de Datos** | 6 |
| **Vistas** | 30+ |
| **Formularios** | 8 |
| **Tests** | En desarrollo |

</div>

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### 🐛 Reportar Bugs
Usa el [sistema de issues](https://github.com/tu-usuario/GestorInventario/issues) para reportar bugs o sugerir mejoras.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Felipe** - *Desarrollador Principal*

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

---

## 🙏 Agradecimientos

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Team](https://getbootstrap.com/)
- Comunidad de desarrolladores chilenos 🇨🇱

---

<div align="center">

**⭐ ¡Dale una estrella si este proyecto te fue útil! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/GestorInventario?style=social)](https://github.com/tu-usuario/GestorInventario/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/tu-usuario/GestorInventario?style=social)](https://github.com/tu-usuario/GestorInventario/network)

</div>

---

<div align="center">
<sub>Hecho con ❤️ en Chile 🇨🇱</sub>
</div>
