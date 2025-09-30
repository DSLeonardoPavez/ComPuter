import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Button, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia,
  Chip,
  Stack,
  Paper,
  Avatar,
  Rating
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import BuildIcon from '@mui/icons-material/Build';
import SpeedIcon from '@mui/icons-material/Speed';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SecurityIcon from '@mui/icons-material/Security';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';

const HomePage = () => {
  const features = [
    {
      icon: <SmartToyIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'IA Avanzada',
      description: 'Motor de recomendaciones inteligente que aprende de tus preferencias y necesidades específicas.'
    },
    {
      icon: <BuildIcon sx={{ fontSize: 40, color: 'secondary.main' }} />,
      title: 'Compatibilidad Garantizada',
      description: 'Verificación automática de compatibilidad entre componentes para evitar problemas.'
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 40, color: 'success.main' }} />,
      title: 'Optimización de Rendimiento',
      description: 'Configuraciones optimizadas para gaming, trabajo profesional, streaming y más.'
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 40, color: 'warning.main' }} />,
      title: 'Datos Actualizados',
      description: 'Base de datos constantemente actualizada con los últimos componentes del mercado.'
    },
    {
      icon: <TrendingUpIcon sx={{ fontSize: 40, color: 'info.main' }} />,
      title: 'Análisis de Precios',
      description: 'Comparación de precios en tiempo real para encontrar las mejores ofertas.'
    },
    {
      icon: <SupportAgentIcon sx={{ fontSize: 40, color: 'error.main' }} />,
      title: 'Soporte 24/7',
      description: 'Chatbot inteligente disponible las 24 horas para resolver tus dudas.'
    }
  ];

  const testimonials = [
    {
      name: 'Carlos Rodríguez',
      role: 'Gamer Profesional',
      rating: 5,
      comment: 'Increíble sistema de recomendaciones. Me ayudó a armar mi PC gaming perfecta dentro de mi presupuesto.',
      avatar: '/avatars/carlos.jpg'
    },
    {
      name: 'Ana García',
      role: 'Diseñadora Gráfica',
      rating: 5,
      comment: 'La compatibilidad automática me ahorró horas de investigación. Excelente para profesionales.',
      avatar: '/avatars/ana.jpg'
    },
    {
      name: 'Miguel Torres',
      role: 'Streamer',
      rating: 4,
      comment: 'Perfecto para encontrar componentes optimizados para streaming. Muy recomendado.',
      avatar: '/avatars/miguel.jpg'
    }
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: { xs: 8, md: 12 },
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Container maxWidth="lg">
          <Typography 
            variant="h2" 
            component="h1" 
            gutterBottom
            sx={{ 
              fontWeight: 'bold',
              fontSize: { xs: '2.5rem', md: '3.5rem' },
              mb: 3
            }}
          >
            Construye tu PC Perfecta
          </Typography>
          <Typography 
            variant="h5" 
            paragraph
            sx={{ 
              mb: 4,
              opacity: 0.9,
              maxWidth: '600px',
              mx: 'auto'
            }}
          >
            Sistema inteligente de recomendación de componentes con IA avanzada, 
            verificación de compatibilidad y análisis de precios en tiempo real.
          </Typography>
          
          <Stack 
            direction={{ xs: 'column', sm: 'row' }} 
            spacing={2} 
            justifyContent="center"
            sx={{ mb: 6 }}
          >
            <Button
              component={RouterLink}
              to="/profile"
              variant="contained"
              color="secondary"
              size="large"
              sx={{ 
                px: 4, 
                py: 1.5,
                fontSize: '1.1rem',
                borderRadius: 3,
                boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
              }}
            >
              Comenzar Ahora
            </Button>
            <Button
              component={RouterLink}
              to="/search"
              variant="outlined"
              size="large"
              sx={{ 
                px: 4, 
                py: 1.5,
                fontSize: '1.1rem',
                borderRadius: 3,
                borderColor: 'white',
                color: 'white',
                '&:hover': {
                  borderColor: 'white',
                  backgroundColor: 'rgba(255,255,255,0.1)'
                }
              }}
            >
              Explorar Componentes
            </Button>
          </Stack>

          <Stack direction="row" spacing={4} justifyContent="center" flexWrap="wrap">
            <Chip 
              label="🚀 IA Avanzada" 
              sx={{ 
                backgroundColor: 'rgba(255,255,255,0.2)', 
                color: 'white',
                fontSize: '0.9rem',
                py: 2
              }} 
            />
            <Chip 
              label="⚡ Compatibilidad Automática" 
              sx={{ 
                backgroundColor: 'rgba(255,255,255,0.2)', 
                color: 'white',
                fontSize: '0.9rem',
                py: 2
              }} 
            />
            <Chip 
              label="💰 Mejores Precios" 
              sx={{ 
                backgroundColor: 'rgba(255,255,255,0.2)', 
                color: 'white',
                fontSize: '0.9rem',
                py: 2
              }} 
            />
          </Stack>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography 
          variant="h3" 
          component="h2" 
          textAlign="center" 
          gutterBottom
          sx={{ mb: 6, fontWeight: 'bold' }}
        >
          ¿Por qué elegir ComPuter?
        </Typography>
        
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} lg={4} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 12px 40px rgba(0,0,0,0.15)'
                  },
                  borderRadius: 3,
                  border: '1px solid rgba(0,0,0,0.05)'
                }}
              >
                <CardContent sx={{ p: 4, textAlign: 'center' }}>
                  <Box sx={{ mb: 3 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" component="h3" gutterBottom sx={{ fontWeight: 'bold' }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Stats Section */}
      <Box sx={{ backgroundColor: 'grey.50', py: 8 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} textAlign="center">
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="h3" color="primary.main" sx={{ fontWeight: 'bold', mb: 1 }}>
                10K+
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Componentes en Base de Datos
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="h3" color="secondary.main" sx={{ fontWeight: 'bold', mb: 1 }}>
                5K+
              </Typography>
              <Typography variant="h6" color="text.secondary">
                PCs Configuradas
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="h3" color="success.main" sx={{ fontWeight: 'bold', mb: 1 }}>
                98%
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Compatibilidad Garantizada
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="h3" color="warning.main" sx={{ fontWeight: 'bold', mb: 1 }}>
                24/7
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Soporte Disponible
              </Typography>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Testimonials Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography 
          variant="h3" 
          component="h2" 
          textAlign="center" 
          gutterBottom
          sx={{ mb: 6, fontWeight: 'bold' }}
        >
          Lo que dicen nuestros usuarios
        </Typography>
        
        <Grid container spacing={4}>
          {testimonials.map((testimonial, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Paper 
                elevation={2}
                sx={{ 
                  p: 4, 
                  height: '100%',
                  borderRadius: 3,
                  transition: 'transform 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-4px)'
                  }
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar 
                    src={testimonial.avatar}
                    sx={{ width: 56, height: 56, mr: 2 }}
                  >
                    {testimonial.name.charAt(0)}
                  </Avatar>
                  <Box>
                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                      {testimonial.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {testimonial.role}
                    </Typography>
                  </Box>
                </Box>
                
                <Rating value={testimonial.rating} readOnly sx={{ mb: 2 }} />
                
                <Typography variant="body1" sx={{ fontStyle: 'italic', lineHeight: 1.6 }}>
                  "{testimonial.comment}"
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box 
        sx={{ 
          backgroundColor: 'primary.main',
          color: 'white',
          py: 8,
          textAlign: 'center'
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 'bold' }}>
            ¿Listo para construir tu PC ideal?
          </Typography>
          <Typography variant="h6" paragraph sx={{ mb: 4, opacity: 0.9 }}>
            Únete a miles de usuarios que ya han encontrado su configuración perfecta
          </Typography>
          <Button
            component={RouterLink}
            to="/profile"
            variant="contained"
            color="secondary"
            size="large"
            sx={{ 
              px: 6, 
              py: 2,
              fontSize: '1.2rem',
              borderRadius: 3,
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
            }}
          >
            Comenzar Gratis
          </Button>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;