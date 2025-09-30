import React, { useState } from 'react';

import {
  Container,
  Typography,
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Paper,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Slider,
  Checkbox,
  Grid,
  Card,
  CardContent,
  Alert
} from '@mui/material';

const UserProfileWizard = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [userData, setUserData] = useState({
    email: '',
    name: '',
    usageType: 'gaming',
    budget: 1000,
    preferences: {
      prioritizePerformance: true,
      prioritizeSilence: false,
      prioritizeAesthetics: false,
      prioritizePrice: false,
    }
  });

  const steps = ['Información básica', 'Tipo de uso', 'Presupuesto', 'Preferencias', 'Resumen'];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleSubmit = () => {
    // Aquí se enviarían los datos a la API
    console.log('Datos del perfil:', userData);
    // Avanzar al paso final
    handleNext();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserData({
      ...userData,
      [name]: value
    });
  };

  const handleUsageTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserData({
      ...userData,
      usageType: e.target.value
    });
  };

  const handleBudgetChange = (event: Event, newValue: number | number[]) => {
    setUserData({
      ...userData,
      budget: newValue as number
    });
  };

  const handlePreferenceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setUserData({
      ...userData,
      preferences: {
        ...userData.preferences,
        [name]: checked
      }
    });
  };

  const getStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Información básica
            </Typography>
            <TextField
              fullWidth
              margin="normal"
              label="Nombre"
              name="name"
              value={userData.name}
              onChange={handleInputChange}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Correo electrónico"
              name="email"
              type="email"
              value={userData.email}
              onChange={handleInputChange}
            />
          </Box>
        );
      case 1:
        return (
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              ¿Para qué usarás principalmente tu PC?
            </Typography>
            <FormControl component="fieldset">
              <RadioGroup
                name="usageType"
                value={userData.usageType}
                onChange={handleUsageTypeChange}
              >
                <FormControlLabel value="gaming" control={<Radio />} label="Gaming" />
                <FormControlLabel value="workstation" control={<Radio />} label="Estación de trabajo (diseño, edición)" />
                <FormControlLabel value="office" control={<Radio />} label="Ofimática y navegación" />
                <FormControlLabel value="development" control={<Radio />} label="Desarrollo de software" />
                <FormControlLabel value="streaming" control={<Radio />} label="Streaming y creación de contenido" />
              </RadioGroup>
            </FormControl>
          </Box>
        );
      case 2:
        return (
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              ¿Cuál es tu presupuesto aproximado?
            </Typography>
            <Box sx={{ px: 3 }}>
              <Typography gutterBottom>
                Presupuesto: ${userData.budget}
              </Typography>
              <Slider
                value={userData.budget}
                onChange={handleBudgetChange}
                min={500}
                max={5000}
                step={100}
                marks={[
                  { value: 500, label: '$500' },
                  { value: 1000, label: '$1000' },
                  { value: 2000, label: '$2000' },
                  { value: 3000, label: '$3000' },
                  { value: 5000, label: '$5000' },
                ]}
                valueLabelDisplay="auto"
              />
            </Box>
          </Box>
        );
      case 3:
        return (
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Preferencias
            </Typography>
            <FormControl component="fieldset">
              <FormLabel component="legend">Selecciona tus prioridades:</FormLabel>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={userData.preferences.prioritizePerformance}
                    onChange={handlePreferenceChange}
                    name="prioritizePerformance"
                  />
                }
                label="Priorizar rendimiento"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={userData.preferences.prioritizeSilence}
                    onChange={handlePreferenceChange}
                    name="prioritizeSilence"
                  />
                }
                label="Priorizar silencio (menos ruido)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={userData.preferences.prioritizeAesthetics}
                    onChange={handlePreferenceChange}
                    name="prioritizeAesthetics"
                  />
                }
                label="Priorizar estética (iluminación RGB, diseño)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={userData.preferences.prioritizePrice}
                    onChange={handlePreferenceChange}
                    name="prioritizePrice"
                  />
                }
                label="Priorizar relación calidad-precio"
              />
            </FormControl>
          </Box>
        );
      case 4:
        return (
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Resumen de tu perfil
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1">Información personal</Typography>
                    <Typography variant="body2">Nombre: {userData.name}</Typography>
                    <Typography variant="body2">Email: {userData.email}</Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1">Uso principal</Typography>
                    <Typography variant="body2">{userData.usageType}</Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1">Presupuesto</Typography>
                    <Typography variant="body2">${userData.budget}</Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1">Preferencias</Typography>
                    <Typography variant="body2">
                      {userData.preferences.prioritizePerformance && "• Priorizar rendimiento"}
                    </Typography>
                    <Typography variant="body2">
                      {userData.preferences.prioritizeSilence && "• Priorizar silencio"}
                    </Typography>
                    <Typography variant="body2">
                      {userData.preferences.prioritizeAesthetics && "• Priorizar estética"}
                    </Typography>
                    <Typography variant="body2">
                      {userData.preferences.prioritizePrice && "• Priorizar relación calidad-precio"}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        );
      default:
        return (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <Alert severity="success" sx={{ mb: 3 }}>
              ¡Tu perfil ha sido creado con éxito!
            </Alert>
            <Typography variant="h6" gutterBottom>
              Ahora puedes obtener recomendaciones personalizadas
            </Typography>
            <Button
              variant="contained"
              color="primary"
              sx={{ mt: 2 }}
              onClick={() => {
                // Aquí se navegaría a la página de recomendaciones
                console.log('Ir a recomendaciones');
              }}
            >
              Ver mis recomendaciones
            </Button>
          </Box>
        );
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Asistente de Perfil
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Configura tu perfil para obtener recomendaciones personalizadas
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Paper elevation={3} sx={{ mb: 4 }}>
        {activeStep === steps.length ? (
          getStepContent(steps.length)
        ) : (
          <>
            {getStepContent(activeStep)}
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 3 }}>
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
                sx={{ mr: 1 }}
              >
                Atrás
              </Button>
              {activeStep === steps.length - 1 ? (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                >
                  Finalizar
                </Button>
              ) : (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext}
                >
                  Siguiente
                </Button>
              )}
            </Box>
          </>
        )}
      </Paper>
    </Container>
  );
};

export default UserProfileWizard;