import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
  CircularProgress,
  Chip,
  Snackbar
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import { compareComponents } from '../services/api';

// Tipos para los componentes
interface Specification {
  name: string;
  value: string;
}

interface Component {
  id: number;
  name: string;
  type: string;
  brand: string;
  model: string;
  price: number;
  performance_score: number;
  power_consumption: number;
  specifications: Specification[];
}

interface CompatibilityResult {
  compatible: boolean;
  message: string;
  issues: string[];
  compatibility_score: number;
}

interface ComparisonResult {
  components: Record<string, Component[]>;
  compatibility: CompatibilityResult;
  summary: {
    total_price: number;
    average_performance: number;
    total_power_consumption: number;
    component_count: number;
  };
}

const ComparisonTool = () => {
  // Estado para los componentes seleccionados
  const [selectedComponents, setSelectedComponents] = useState<Component[]>([
    {
      id: 1,
      name: 'AMD Ryzen 7 5800X',
      type: 'CPU',
      brand: 'AMD',
      model: 'Ryzen 7 5800X',
      price: 349.99,
      performance_score: 87.5,
      power_consumption: 105,
      specifications: [
        { name: 'cores', value: '8' },
        { name: 'threads', value: '16' },
        { name: 'base_clock', value: '3.8 GHz' },
        { name: 'socket', value: 'AM4' }
      ]
    },
    {
      id: 3,
      name: 'NVIDIA GeForce RTX 3080',
      type: 'GPU',
      brand: 'NVIDIA',
      model: 'GeForce RTX 3080',
      price: 699.99,
      performance_score: 94.5,
      power_consumption: 320,
      specifications: [
        { name: 'memory', value: '10 GB GDDR6X' },
        { name: 'boost_clock', value: '1.71 GHz' },
        { name: 'cuda_cores', value: '8704' }
      ]
    },
    {
      id: 4,
      name: 'Corsair Vengeance RGB Pro 32GB',
      type: 'RAM',
      brand: 'Corsair',
      model: 'Vengeance RGB Pro',
      price: 149.99,
      performance_score: 85.0,
      power_consumption: 10,
      specifications: [
        { name: 'capacity', value: '32 GB (2x16GB)' },
        { name: 'speed', value: '3600 MHz' },
        { name: 'type', value: 'DDR4' }
      ]
    }
  ]);

  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);

  // Función para verificar compatibilidad usando la API real
  const checkCompatibility = async () => {
    if (selectedComponents.length === 0) {
      setError('No hay componentes seleccionados para comparar');
      setSnackbarOpen(true);
      return;
    }

    setLoading(true);
    try {
      const componentIds = selectedComponents.map(comp => comp.id);
      const result = await compareComponents(componentIds);
      setComparisonResult(result);
      setError('');
    } catch (err) {
      console.error('Error checking compatibility:', err);
      setError('Error al verificar compatibilidad. Usando datos de ejemplo.');
      setSnackbarOpen(true);
      
      // Fallback a datos de ejemplo si la API falla
      setComparisonResult({
        components: groupComponentsByType(selectedComponents),
        compatibility: {
          compatible: true,
          message: 'Los componentes son compatibles',
          issues: [],
          compatibility_score: 85.5
        },
        summary: {
          total_price: selectedComponents.reduce((sum, comp) => sum + comp.price, 0),
          average_performance: selectedComponents.reduce((sum, comp) => sum + comp.performance_score, 0) / selectedComponents.length,
          total_power_consumption: selectedComponents.reduce((sum, comp) => sum + comp.power_consumption, 0),
          component_count: selectedComponents.length
        }
      });
    } finally {
      setLoading(false);
    }
  };

  // Función auxiliar para agrupar componentes por tipo
  const groupComponentsByType = (components: Component[]): Record<string, Component[]> => {
    const grouped: Record<string, Component[]> = {};
    components.forEach(component => {
      if (!grouped[component.type]) {
        grouped[component.type] = [];
      }
      grouped[component.type].push(component);
    });
    return grouped;
  };

  // Función para eliminar un componente de la comparación
  const removeComponent = (componentId: number) => {
    setSelectedComponents(selectedComponents.filter(comp => comp.id !== componentId));
    setComparisonResult(null); // Resetear resultado al cambiar componentes
  };

  // Ejecutar verificación automáticamente cuando cambien los componentes
  useEffect(() => {
    if (selectedComponents.length > 0) {
      checkCompatibility();
    }
  }, [selectedComponents]);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Comparación de Componentes
      </Typography>

      {/* Resumen de componentes seleccionados */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Componentes seleccionados
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {selectedComponents.map((component) => (
            <Chip
              key={component.id}
              label={`${component.type}: ${component.name}`}
              onDelete={() => removeComponent(component.id)}
              color="primary"
            />
          ))}
        </Box>
        <Box sx={{ mt: 2 }}>
          <Button 
            variant="contained" 
            onClick={checkCompatibility}
            disabled={loading || selectedComponents.length === 0}
          >
            {loading ? <CircularProgress size={24} /> : 'Verificar Compatibilidad'}
          </Button>
        </Box>
      </Box>

      {/* Resultado de compatibilidad */}
      {comparisonResult && (
        <Box sx={{ mb: 4 }}>
          <Alert 
            severity={comparisonResult.compatibility.compatible ? "success" : "error"}
            icon={comparisonResult.compatibility.compatible ? <CheckCircleIcon /> : <ErrorIcon />}
          >
            <Box>
              <Typography variant="h6">
                {comparisonResult.compatibility.message}
              </Typography>
              <Typography variant="body2">
                Puntuación de compatibilidad: {comparisonResult.compatibility.compatibility_score.toFixed(1)}/100
              </Typography>
              {comparisonResult.compatibility.issues.length > 0 && (
                <Box sx={{ mt: 1 }}>
                  <Typography variant="body2" fontWeight="bold">Problemas encontrados:</Typography>
                  <ul>
                    {comparisonResult.compatibility.issues.map((issue, index) => (
                      <li key={index}>{issue}</li>
                    ))}
                  </ul>
                </Box>
              )}
            </Box>
          </Alert>
        </Box>
      )}

      {/* Tablas de comparación por tipo de componente */}
      {comparisonResult && Object.entries(comparisonResult.components).map(([type, components]) => (
        <Box key={type} sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            {type}
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Especificación</TableCell>
                  {components.map(component => (
                    <TableCell key={component.id}>{component.name}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>Marca</TableCell>
                  {components.map(component => (
                    <TableCell key={component.id}>{component.brand}</TableCell>
                  ))}
                </TableRow>
                <TableRow>
                  <TableCell>Modelo</TableCell>
                  {components.map(component => (
                    <TableCell key={component.id}>{component.model}</TableCell>
                  ))}
                </TableRow>
                <TableRow>
                  <TableCell>Precio</TableCell>
                  {components.map(component => (
                    <TableCell key={component.id}>${component.price.toFixed(2)}</TableCell>
                  ))}
                </TableRow>
                <TableRow>
                  <TableCell>Rendimiento</TableCell>
                  {components.map(component => (
                    <TableCell key={component.id}>{component.performance_score}/100</TableCell>
                  ))}
                </TableRow>
                <TableRow>
                  <TableCell>Consumo</TableCell>
                  {components.map(component => (
                    <TableCell key={component.id}>{component.power_consumption}W</TableCell>
                  ))}
                </TableRow>
                {/* Especificaciones específicas */}
                {getUniqueSpecKeys(components).map(specKey => (
                  <TableRow key={specKey}>
                    <TableCell>{specKey.replace('_', ' ')}</TableCell>
                    {components.map(component => {
                      const spec = component.specifications.find(s => s.name === specKey);
                      return (
                        <TableCell key={component.id}>
                          {spec ? spec.value : '-'}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      ))}

      {/* Resumen de costos y rendimiento */}
      {comparisonResult && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>Resumen</Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <Typography variant="h6">Costo Total</Typography>
                <Typography variant="h4" color="primary">
                  ${comparisonResult.summary.total_price.toFixed(2)}
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="h6">Rendimiento Promedio</Typography>
                <Typography variant="h4" color="secondary">
                  {comparisonResult.summary.average_performance.toFixed(1)}/100
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="h6">Consumo Total</Typography>
                <Typography variant="h4">
                  {comparisonResult.summary.total_power_consumption}W
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="h6">Componentes</Typography>
                <Typography variant="h4">
                  {comparisonResult.summary.component_count}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Botones de acción */}
      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
        <Button variant="outlined" color="primary">
          Guardar Configuración
        </Button>
        <Button variant="contained" color="secondary">
          Obtener Recomendaciones
        </Button>
      </Box>

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

// Función auxiliar para obtener claves únicas de especificaciones
const getUniqueSpecKeys = (components: Component[]): string[] => {
  const allKeys = new Set<string>();
  components.forEach(component => {
    component.specifications.forEach(spec => {
      allKeys.add(spec.name);
    });
  });
  return Array.from(allKeys);
};

export default ComparisonTool;