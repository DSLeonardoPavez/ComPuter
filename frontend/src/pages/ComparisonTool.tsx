import React, { useState } from 'react';
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
  Chip
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';

// Tipos para los componentes
interface Specification {
  key: string;
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
  is_compatible: boolean;
  issues: string[];
  compatibility_score: number;
}

const ComparisonTool = () => {
  // Estado para los componentes seleccionados (en una aplicación real, esto vendría de un estado global o URL)
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
        { key: 'cores', value: '8' },
        { key: 'threads', value: '16' },
        { key: 'base_clock', value: '3.8 GHz' },
        { key: 'socket', value: 'AM4' }
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
        { key: 'memory', value: '10 GB GDDR6X' },
        { key: 'boost_clock', value: '1.71 GHz' },
        { key: 'cuda_cores', value: '8704' }
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
        { key: 'capacity', value: '32 GB (2x16GB)' },
        { key: 'speed', value: '3600 MHz' },
        { key: 'type', value: 'DDR4' }
      ]
    }
  ]);

  const [compatibilityResult, setCompatibilityResult] = useState<CompatibilityResult | null>({
    is_compatible: true,
    issues: [],
    compatibility_score: 0.95
  });

  const [checkingCompatibility, setCheckingCompatibility] = useState<boolean>(false);

  // Función para verificar compatibilidad (en producción, esto sería una llamada a la API)
  const checkCompatibility = () => {
    setCheckingCompatibility(true);
    
    // Simular llamada a la API
    setTimeout(() => {
      // Ejemplo de resultado
      setCompatibilityResult({
        is_compatible: true,
        issues: [],
        compatibility_score: 0.95
      });
      setCheckingCompatibility(false);
    }, 1500);
  };

  // Función para eliminar un componente de la comparación
  const removeComponent = (componentId: number) => {
    setSelectedComponents(selectedComponents.filter(comp => comp.id !== componentId));
    // Resetear el resultado de compatibilidad si cambian los componentes
    setCompatibilityResult(null);
  };

  // Agrupar componentes por tipo para la tabla de comparación
  const componentsByType: Record<string, Component[]> = {};
  selectedComponents.forEach(component => {
    if (!componentsByType[component.type]) {
      componentsByType[component.type] = [];
    }
    componentsByType[component.type].push(component);
  });

  // Obtener todas las especificaciones únicas para cada tipo de componente
  const specKeysByType: Record<string, string[]> = {};
  Object.entries(componentsByType).forEach(([type, components]) => {
    const allKeys = new Set<string>();
    components.forEach(component => {
      component.specifications.forEach(spec => {
        allKeys.add(spec.key);
      });
    });
    specKeysByType[type] = Array.from(allKeys);
  });

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
      </Box>

      {/* Botón para verificar compatibilidad */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'center' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={checkCompatibility}
          disabled={checkingCompatibility || selectedComponents.length < 2}
          sx={{ minWidth: 200 }}
        >
          {checkingCompatibility ? (
            <>
              <CircularProgress size={24} sx={{ mr: 1, color: 'white' }} />
              Verificando...
            </>
          ) : (
            'Verificar Compatibilidad'
          )}
        </Button>
      </Box>

      {/* Resultado de compatibilidad */}
      {compatibilityResult && (
        <Box sx={{ mb: 4 }}>
          <Alert
            severity={compatibilityResult.is_compatible ? "success" : "error"}
            icon={compatibilityResult.is_compatible ? <CheckCircleIcon /> : <ErrorIcon />}
          >
            <Typography variant="h6">
              {compatibilityResult.is_compatible
                ? "¡Los componentes son compatibles!"
                : "Hay problemas de compatibilidad"}
            </Typography>
            <Typography>
              Puntuación de compatibilidad: {(compatibilityResult.compatibility_score * 100).toFixed(0)}%
            </Typography>
            {compatibilityResult.issues.length > 0 && (
              <Box sx={{ mt: 1 }}>
                <Typography variant="subtitle2">Problemas detectados:</Typography>
                <ul>
                  {compatibilityResult.issues.map((issue, index) => (
                    <li key={index}>{issue}</li>
                  ))}
                </ul>
              </Box>
            )}
          </Alert>
        </Box>
      )}

      {/* Tablas de comparación por tipo de componente */}
      {Object.entries(componentsByType).map(([type, components]) => (
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
                {specKeysByType[type].map(specKey => (
                  <TableRow key={specKey}>
                    <TableCell>{specKey.replace('_', ' ')}</TableCell>
                    {components.map(component => {
                      const spec = component.specifications.find(s => s.key === specKey);
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
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6">Costo Total</Typography>
              <Typography variant="h4" color="primary">
                ${selectedComponents.reduce((sum, comp) => sum + comp.price, 0).toFixed(2)}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6">Rendimiento Promedio</Typography>
              <Typography variant="h4" color="secondary">
                {(selectedComponents.reduce((sum, comp) => sum + comp.performance_score, 0) / 
                  (selectedComponents.length || 1)).toFixed(1)}/100
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6">Consumo Total</Typography>
              <Typography variant="h4">
                {selectedComponents.reduce((sum, comp) => sum + comp.power_consumption, 0)}W
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Botones de acción */}
      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
        <Button variant="outlined" color="primary">
          Guardar Configuración
        </Button>
        <Button variant="contained" color="secondary">
          Obtener Recomendaciones
        </Button>
      </Box>
    </Container>
  );
};

export default ComparisonTool;