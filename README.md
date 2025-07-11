# 📦 GestorInventario

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**Sistema de Gestión de Inventario Completo para Empresas Chilenas**

[🚀 Demo](#demo) • [📥 Instalación](#instalación) • [📖 Documentación](#documentación) • [🎯 Alcances](#alcances) • [🤝 Contribuir](#contribuir)

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
- ✅ Alertas de stock bajo

### 🛒 **Sistema de Ventas**
- ✅ Carrito interactivo con animaciones
- ✅ Códigos de boleta secuenciales chilenos
- ✅ Recibos estilo boleta tradicional
- ✅ Tracking completo de transacciones
- ✅ Validación de datos en tiempo real

</td>
<td width="50%">

### 👥 **Gestión de Usuarios**
- ✅ Sistema de roles (Admin/Staff/Usuario)
- ✅ Validación RUT chileno completa
- ✅ Perfiles con estadísticas personalizadas
- ✅ Control de permisos granular
- ✅ Historial de actividades

### 🏢 **Proveedores**
- ✅ Base de datos de proveedores
- ✅ Información de contacto completa
- ✅ Validación de datos empresariales
- ✅ Asociación con productos

</td>
</tr>
</table>

---

## 🎯 Alcances del Proyecto

### 📋 **Alcances Funcionales**

#### ✅ **Implementados**
- **Gestión Completa de Inventario**: CRUD de productos, categorías y proveedores
- **Sistema de Ventas**: Carrito de compras, checkout y generación de boletas
- **Gestión de Usuarios**: Registro, login, perfiles y control de permisos
- **Validaciones Chilenas**: RUT, formatos de fecha y moneda
- **Importación de Datos**: Carga masiva desde archivos Excel
- **Interfaz Responsive**: Compatible con dispositivos móviles y desktop
- **Historial de Transacciones**: Seguimiento completo de movimientos

#### 🔄 **En Desarrollo**
- **Reportes Avanzados**: Gráficos y estadísticas detalladas
- **Notificaciones**: Alertas por email y en tiempo real
- **API REST**: Endpoints para integración con otros sistemas
- **Backup Automático**: Respaldo automático de datos

#### 🔮 **Planificados**
- **Integración con Sistemas Externos**: Conexión con contabilidad
- **Módulo de Compras**: Gestión de órdenes de compra
- **Control de Calidad**: Seguimiento de productos defectuosos
- **Multi-empresa**: Soporte para múltiples empresas

### 🚀 **Alcances Técnicos**

#### ✅ **Arquitectura Actual**
- **Framework**: Django 5.2.1 con arquitectura MVT
- **Base de Datos**: SQLite3 (desarrollo) / PostgreSQL (producción)
- **Frontend**: Bootstrap 5.3 + JavaScript Vanilla
- **Autenticación**: Sistema Django integrado
- **Validaciones**: Frontend (JS) + Backend (Django)

#### 📊 **Capacidades**
- **Usuarios Concurrentes**: Hasta 50 usuarios simultáneos
- **Productos**: Sin límite teórico (optimizado para ~10,000)
- **Transacciones**: Histórico completo sin límites
- **Archivos**: Soporte para Excel (.xlsx, .xls)
- **Tamaño de BD**: SQLite hasta 281 TB teórico

#### 🔒 **Seguridad**
- **Autenticación**: Login seguro con hash de contraseñas
- **Autorización**: Decoradores de permisos personalizados
- **Validaciones**: Doble validación (frontend + backend)
- **CSRF Protection**: Protección contra ataques CSRF
- **SQL Injection**: Prevención mediante Django ORM

### 🎯 **Casos de Uso Objetivo**

<table>
<tr>
<td width="33%">

#### 🏪 **Pequeños Comercios**
- **Tamaño**: 1-5 usuarios
- **Productos**: 100-1,000 items
- **Ventas**: 10-100 diarias
- **Uso**: Control básico de inventario

</td>
<td width="33%">

#### 🏭 **Talleres y Fábricas**
- **Tamaño**: 5-20 usuarios
- **Productos**: 500-5,000 items
- **Movimientos**: 50-500 diarios
- **Uso**: Control de materiales y consumos

</td>
<td width="33%">

#### 🏢 **Oficinas y Servicios**
- **Tamaño**: 3-15 usuarios
- **Productos**: 200-2,000 items
- **Requisiciones**: 20-200 diarias
- **Uso**: Suministros y activos

</td>
</tr>
</table>

---

## 🖼️ Capturas de Pantalla

<div align="center">

### Dashboard Principal
*Vista general del sistema con métricas clave*

### Sistema de Carrito
*Carrito interactivo con contador dinámico y validaciones*

### Gestión de Productos
*Formularios intuitivos con validaciones en tiempo real*

### Reportes y Historial
*Seguimiento completo de transacciones y movimientos*

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

| **Categoría** | **Tecnología** | **Versión** | **Propósito** |
|---------------|----------------|-------------|---------------|
| **Backend** | Django | 5.2.1 | Framework web principal |
| **Language** | Python | 3.7+ | Lenguaje de programación |
| **Frontend** | Bootstrap | 5.3 | Framework CSS |
| **Database** | SQLite3 | - | Base de datos (desarrollo) |
| **Validation** | JavaScript | ES6+ | Validaciones del lado cliente |
| **Icons** | SVG | - | Iconografía personalizada |
| **Files** | openpyxl | - | Procesamiento de Excel |

</div>

---

## 📋 Funcionalidades Específicas para Chile

### 🇨🇱 **Adaptado al Mercado Chileno**
- **Validación RUT**: Algoritmo completo para personas y empresas
- **Códigos de Boleta**: Sistema secuencial BOL-00000001, BOL-00000002...
- **Moneda Chilena**: Precios en pesos chilenos (formato: $1.234.567)
- **Formato de Fechas**: DD/MM/YYYY según estándar chileno
- **Terminología Local**: Adaptado al lenguaje comercial chileno

---

## 📖 Estructura del Proyecto

```
GestorInventario/
├── 📁 inventory/                    # App principal
│   ├── 📁 static/                   # Archivos estáticos
│   │   ├── 📁 css/                  # Estilos personalizados
│   │   ├── 📁 js/                   # JavaScript
│   │   └── 📁 images/               # Imágenes y iconos
│   ├── 📁 templates/                # Plantillas HTML
│   │   └── 📁 inv/                  # Templates específicos
│   ├── 📁 templatetags/             # Filtros personalizados
│   ├── 📁 migrations/               # Migraciones de BD
│   ├── 📄 models.py                 # 6 modelos principales
│   ├── 📄 views.py                  # 30+ vistas (937 líneas)
│   ├── 📄 forms.py                  # 8 formularios con validaciones
│   ├── 📄 urls.py                   # 20+ endpoints
│   ├── 📄 admin.py                  # Configuración admin
│   ├── 📄 decorators.py             # Decoradores personalizados
│   └── 📄 validators.py             # Validaciones personalizadas
├── 📁 inventory_management_system/  # Configuración Django
│   ├── 📄 settings.py               # Configuración principal
│   ├── 📄 urls.py                   # URLs principales
│   └── 📄 wsgi.py                   # Configuración WSGI
├── 📁 staticfiles/                  # Archivos estáticos compilados
├── 📄 db.sqlite3                   # Base de datos SQLite
├── 📄 requirements.txt             # Dependencias Python
├── 📄 productos.xlsx               # Archivo ejemplo
├── 📄 Dockerfile                   # Configuración Docker
└── 📄 manage.py                    # Script de administración Django
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno (Producción)
```bash
# Archivo .env
DEBUG=False
SECRET_KEY=tu-secret-key-super-segura-aqui
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-app
```

### Configuración Docker
```dockerfile
# Construcción
docker build -t gestor-inventario .

# Ejecución
docker run -p 8000:8000 -e DEBUG=False gestor-inventario

# Con variables de entorno
docker run -p 8000:8000 --env-file .env gestor-inventario
```

---

## 📊 Métricas del Proyecto

<div align="center">

| **Métrica** | **Valor** | **Descripción** |
|-------------|-----------|-----------------|
| **Líneas de Código** | ~3,500+ | Código Python + JavaScript |
| **Plantillas HTML** | 20+ | Templates responsive |
| **Modelos de Datos** | 6 | Producto, Usuario, Venta, etc. |
| **Vistas** | 30+ | Controladores de lógica |
| **Formularios** | 8 | Con validaciones completas |
| **Endpoints** | 20+ | URLs del sistema |
| **Archivos CSS** | 3 | Estilos personalizados |
| **Archivos JS** | 2 | Lógica del cliente |

</div>

---

## 🧪 Testing y Calidad

### Estado Actual
- **Tests Unitarios**: En desarrollo
- **Tests de Integración**: Planificados
- **Validaciones**: Implementadas (frontend + backend)
- **Code Quality**: Siguiendo PEP 8

### Comandos de Testing
```bash
# Ejecutar tests (cuando estén implementados)
python manage.py test

# Verificar coverage
coverage run --source='.' manage.py test
coverage html
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor sigue estos pasos:

### 🔄 **Proceso de Contribución**
1. **Fork** el proyecto
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: Nueva característica increíble'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

### 📝 **Guías de Estilo**
- Sigue **PEP 8** para código Python
- Usa **camelCase** para JavaScript
- Incluye **docstrings** en funciones complejas
- Mantén los **commits** descriptivos

### 🐛 **Reportar Issues**
- Usa el [sistema de issues](https://github.com/tu-usuario/GestorInventario/issues)
- Incluye pasos para reproducir el error
- Adjunta screenshots si es necesario

---

## 📝 Documentación Adicional

- 📖 [Manual de Sistema](MANUAL_DE_SISTEMA.md) - Guía completa de uso
- 🔧 [Guía de Instalación](docs/INSTALACION.md) - Instalación detallada
- 🎯 [Casos de Uso](docs/CASOS_DE_USO.md) - Ejemplos prácticos
- 🔒 [Seguridad](docs/SEGURIDAD.md) - Medidas de seguridad

---

## 🗺️ Roadmap

### Q1 2025
- [ ] Implementar API REST
- [ ] Agregar reportes avanzados
- [ ] Mejorar sistema de notificaciones

### Q2 2025
- [ ] Módulo de compras
- [ ] Integración con contabilidad
- [ ] App móvil nativa

### Q3 2025
- [ ] Soporte multi-empresa
- [ ] Análisis predictivo
- [ ] Exportación a diferentes formatos

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 Felipe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👨‍💻 Autor

**Felipe** - *Desarrollador Principal*

- 🐱 GitHub: [@tu-usuario](https://github.com/tu-usuario)
- 📧 Email: tu-email@ejemplo.com
- 💼 LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---

## 🙏 Agradecimientos

- [Django Documentation](https://docs.djangoproject.com/) - Documentación excelente
- [Bootstrap Team](https://getbootstrap.com/) - Framework CSS robusto
- [Python Community](https://www.python.org/community/) - Comunidad increíble
- **Comunidad de desarrolladores chilenos** 🇨🇱 - Apoyo y feedback

---

## 📞 Soporte

¿Necesitas ayuda? Contáctanos:

- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/GestorInventario/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/GestorInventario/discussions)
- 📧 **Email**: soporte@tudominio.com
- 📱 **WhatsApp**: +56 9 XXXX XXXX

---

<div align="center">

**⭐ ¡Dale una estrella si este proyecto te fue útil! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/GestorInventario?style=social)](https://github.com/tu-usuario/GestorInventario/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/tu-usuario/GestorInventario?style=social)](https://github.com/tu-usuario/GestorInventario/network)
[![GitHub issues](https://img.shields.io/github/issues/tu-usuario/GestorInventario?style=social)](https://github.com/tu-usuario/GestorInventario/issues)

</div>

---

<div align="center">
<sub>Desarrollado con ❤️ en Chile 🇨🇱 | © 2025 Felipe</sub>
</div>