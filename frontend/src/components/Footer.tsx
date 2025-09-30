import React from 'react';
import { Box, Container, Typography, Link, Grid } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import TwitterIcon from '@mui/icons-material/Twitter';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              ComPuter
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Sistema de recomendación de componentes de PC con inteligencia artificial.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Enlaces
            </Typography>
            <Link href="/" color="inherit" display="block">
              Inicio
            </Link>
            <Link href="/search" color="inherit" display="block">
              Buscar Componentes
            </Link>
            <Link href="/compare" color="inherit" display="block">
              Comparar
            </Link>
            <Link href="/profile" color="inherit" display="block">
              Mi Perfil
            </Link>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Síguenos
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Link href="#" color="inherit">
                <GitHubIcon />
              </Link>
              <Link href="#" color="inherit">
                <LinkedInIcon />
              </Link>
              <Link href="#" color="inherit">
                <TwitterIcon />
              </Link>
            </Box>
          </Grid>
        </Grid>
        <Box mt={3}>
          <Typography variant="body2" color="text.secondary" align="center">
            {'© '}
            {new Date().getFullYear()}
            {' ComPuter. Todos los derechos reservados.'}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;