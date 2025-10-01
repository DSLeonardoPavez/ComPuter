import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  CircularProgress,
  Slider,
  FormControlLabel,
  Checkbox,
  Snackbar
} from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { getComponentRecommendations } from '../services/api';

interface Component {
  id: number;
  name: string;
  type: string;
  brand: string;
  model: string;
  price: number;
  performance_score: number;
  power_consumption: number;
  specifications: { name: string; value: string }[];
}

interface RecommendationRequest {
  budget: number;
  use_case: string;
  component_types: string[];
}

interface RecommendationResult {
  recommendations: Component[];
  total_price: number;
  estimated_performance: number;
  total_power_consumption: number;
  explanation: string;
}

const RecommendationTool = () => {
  const [budget, setBudget] = useState<number>(1000);
  const [useCase, setUseCase] = useState<string>('');
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);

  const useCases = [
    { value: 'gaming', label: 'Gaming' },
    { value: 'productivity', label: 'Productividad' },
    { value: 'content_creation', label: 'Creación de Contenido' },
    { value: 'budget', label: 'Presupuesto Ajustado' },
    { value: 'high_performance', label: 'Alto Rendimiento' }
  ];

  const componentTypes = [
    { value: 'CPU', label: 'Procesador (CPU)' },
    { value: 'GPU', label: 'Tarjeta Gráfica (GPU)' },
    { value: 'RAM', label: 'Memoria RAM' },
    { value: 'Storage', label: 'Almacenamiento' },
    { value: 'Motherboard', label: 'Placa Madre' },
    { value: 'PSU', label: 'Fuente de Poder' },
    { value: 'Case', label: 'Gabinete' },
    { value: 'Cooler', label: 'Sistema de Enfriamiento' }
  ];

  const handleUseCaseChange = (event: SelectChangeEvent) => {
    setUseCase(event.target.value);
  };

  const handleTypeToggle = (type: string) => {
    setSelectedTypes(prev => 
      prev.includes(type) 
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  const handleGetRecommendations = async () => {
    if (!useCase) {
      setError('Por favor selecciona un caso de uso');
      setSnackbarOpen(true);
      return;
    }

    if (selectedTypes.length === 0) {
      setError('Por favor selecciona al menos un tipo de componente');
      setSnackbarOpen(true);
      return;
    }

    setLoading(true);
    try {
      const request: RecommendationRequest = {
        budget,
        use_case: useCase,
        component_types: selectedTypes
      };

      const result = await getComponentRecommendations(request);
      setRecommendations(result);
      setError('');
    } catch (err) {
      console.error('Error getting recommendations:', err);
      setError('Error al obtener recomendaciones. Usando datos de ejemplo.');
      setSnackbarOpen(true);
      
      // Fallback a datos de ejemplo
      setRecommendations({
        recommendations: [
          {
            id: 1,
            name: 'AMD Ryzen 5 5600X',
            type: 'CPU',
            brand: 'AMD',
            model: 'Ryzen 5 5600X',
            price: 199.99,
            performance_score: 82.5,
            power_consumption: 65,
            specifications: [
              { name: 'cores', value: '6' },
              { name: 'threads', value: '12' },
              { name: 'base_clock', value: '3.7 GHz' }
            ]
          },
          {
            id: 2,
            name: 'NVIDIA GeForce RTX 3060',
            type: 'GPU',
            brand: 'NVIDIA',
            model: 'GeForce RTX 3060',
            price: 329.99,
            performance_score: 78.0,
            power_consumption: 170,
            specifications: [
              { name: 'memory', value: '12 GB GDDR6' },
              { name: 'boost_clock', value: '1.78 GHz' }
            ]
          }
        ],
        total_price: 529.98,
        estimated_performance: 80.25,
        total_power_consumption: 235,
        explanation: 'Esta configuración ofrece un excelente balance entre precio y rendimiento para gaming en 1080p.'
      });
    } finally {
      setLoading(false);
    }
  };

  const formatBudget = (value: number) => {
    return `$${value.toLocaleString()}`;
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Recomendaciones de Componentes
      </Typography>

      <Grid container spacing={4}>
        {/* Panel de configuración */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Configuración
              </Typography>

              {/* Presupuesto */}
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  Presupuesto: {formatBudget(budget)}
                </Typography>
                <Slider
                  value={budget}
                  onChange={(_, newValue) => setBudget(newValue as number)}
                  min={300}
                  max={5000}
                  step={50}
                  marks={[
                    { value: 300, label: '$300' },
                    { value: 1000, label: '$1K' },
                    { value: 2500, label: '$2.5K' },
                    { value: 5000, label: '$5K' }
                  ]}
                />
              </Box>

              {/* Caso de uso */}
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Caso de Uso</InputLabel>
                <Select
                  value={useCase}
                  label="Caso de Uso"
                  onChange={handleUseCaseChange}
                >
                  {useCases.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Tipos de componentes */}
              <Typography variant="subtitle1" gutterBottom>
                Componentes a incluir:
              </Typography>
              <Box sx={{ mb: 3 }}>
                {componentTypes.map((type) => (
                  <FormControlLabel
                    key={type.value}
                    control={
                      <Checkbox
                        checked={selectedTypes.includes(type.value)}
                        onChange={() => handleTypeToggle(type.value)}
                      />
                    }
                    label={type.label}
                    sx={{ display: 'block' }}
                  />
                ))}
              </Box>

              {/* Botón de recomendaciones */}
              <Button
                variant="contained"
                fullWidth
                onClick={handleGetRecommendations}
                disabled={loading}
                sx={{ mb: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Obtener Recomendaciones'}
              </Button>

              {/* Tipos seleccionados */}
              {selectedTypes.length > 0 && (
                <Box>
                  <Typography variant="subtitle2" gutterBottom>
                    Seleccionados:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selectedTypes.map((type) => (
                      <Chip
                        key={type}
                        label={componentTypes.find(ct => ct.value === type)?.label || type}
                        size="small"
                        onDelete={() => handleTypeToggle(type)}
                      />
                    ))}
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Panel de resultados */}
        <Grid item xs={12} md={8}>
          {recommendations ? (
            <Box>
              {/* Resumen */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Resumen de Recomendaciones
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6} md={3}>
                      <Typography variant="subtitle2">Precio Total</Typography>
                      <Typography variant="h6" color="primary">
                        ${recommendations.total_price.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Typography variant="subtitle2">Rendimiento</Typography>
                      <Typography variant="h6" color="secondary">
                        {recommendations.estimated_performance.toFixed(1)}/100
                      </Typography>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Typography variant="subtitle2">Consumo</Typography>
                      <Typography variant="h6">
                        {recommendations.total_power_consumption}W
                      </Typography>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Typography variant="subtitle2">Componentes</Typography>
                      <Typography variant="h6">
                        {recommendations.recommendations.length}
                      </Typography>
                    </Grid>
                  </Grid>
                  
                  {recommendations.explanation && (
                    <Alert severity="info" sx={{ mt: 2 }}>
                      {recommendations.explanation}
                    </Alert>
                  )}
                </CardContent>
              </Card>

              {/* Lista de componentes recomendados */}
              <Typography variant="h6" gutterBottom>
                Componentes Recomendados
              </Typography>
              <Grid container spacing={2}>
                {recommendations.recommendations.map((component) => (
                  <Grid item xs={12} sm={6} key={component.id}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                          <Chip label={component.type} size="small" color="primary" />
                          <Typography variant="h6" color="primary">
                            ${component.price.toFixed(2)}
                          </Typography>
                        </Box>
                        
                        <Typography variant="h6" gutterBottom>
                          {component.name}
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {component.brand} - {component.model}
                        </Typography>
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                          <Box>
                            <Typography variant="caption" display="block">
                              Rendimiento
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {component.performance_score}/100
                            </Typography>
                          </Box>
                          <Box>
                            <Typography variant="caption" display="block">
                              Consumo
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {component.power_consumption}W
                            </Typography>
                          </Box>
                        </Box>

                        {/* Especificaciones principales */}
                        {component.specifications.length > 0 && (
                          <Box sx={{ mt: 2 }}>
                            <Typography variant="caption" display="block" gutterBottom>
                              Especificaciones:
                            </Typography>
                            {component.specifications.slice(0, 3).map((spec, index) => (
                              <Typography key={index} variant="body2" color="text.secondary">
                                {spec.name}: {spec.value}
                              </Typography>
                            ))}
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>

              {/* Botones de acción */}
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 4 }}>
                <Button variant="outlined">
                  Comparar Componentes
                </Button>
                <Button variant="contained">
                  Guardar Configuración
                </Button>
              </Box>
            </Box>
          ) : (
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 8 }}>
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Configura tus preferencias y obtén recomendaciones personalizadas
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Selecciona tu presupuesto, caso de uso y tipos de componentes para comenzar
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>

      {/* Snackbar para errores */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={() => setSnackbarOpen(false)}
        message={error}
      />
    </Container>
  );
};

export default RecommendationTool;