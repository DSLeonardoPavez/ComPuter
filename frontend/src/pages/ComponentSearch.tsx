import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Chip,
  CircularProgress
} from '@mui/material';

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

const ComponentSearch = () => {
  const [components, setComponents] = useState<Component[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [priceRange, setPriceRange] = useState<number[]>([0, 5000]);
  const [selectedComponents, setSelectedComponents] = useState<Component[]>([]);

  // Tipos de componentes disponibles
  const componentTypes = [
    'CPU', 'GPU', 'RAM', 'Motherboard', 'Storage', 'PSU', 'Case', 'Cooling'
  ];

  // Simular carga de datos (en producción, esto vendría de la API)
  useEffect(() => {
    // Aquí se haría la llamada a la API
    // api.getComponents().then(data => setComponents(data))
    
    // Datos de ejemplo para desarrollo
    const mockComponents: Component[] = [
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
        id: 2,
        name: 'Intel Core i7-12700K',
        type: 'CPU',
        brand: 'Intel',
        model: 'Core i7-12700K',
        price: 389.99,
        performance_score: 92.0,
        power_consumption: 125,
        specifications: [
          { key: 'cores', value: '12' },
          { key: 'threads', value: '20' },
          { key: 'base_clock', value: '3.6 GHz' },
          { key: 'socket', value: 'LGA1700' }
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
    ];
    
    setTimeout(() => {
      setComponents(mockComponents);
      setLoading(false);
    }, 1000);
  }, []);

  // Filtrar componentes según los criterios de búsqueda
  const filteredComponents = components.filter(component => {
    const matchesSearch = component.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         component.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         component.model.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesType = selectedType === '' || component.type === selectedType;
    
    const matchesPrice = component.price >= priceRange[0] && component.price <= priceRange[1];
    
    return matchesSearch && matchesType && matchesPrice;
  });

  // Manejar la selección de componentes
  const handleSelectComponent = (component: Component) => {
    // Verificar si ya está seleccionado
    const isSelected = selectedComponents.some(c => c.id === component.id);
    
    if (isSelected) {
      setSelectedComponents(selectedComponents.filter(c => c.id !== component.id));
    } else {
      setSelectedComponents([...selectedComponents, component]);
    }
  };

  // Manejar cambio en el rango de precios
  const handlePriceChange = (event: Event, newValue: number | number[]) => {
    setPriceRange(newValue as number[]);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Búsqueda de Componentes
      </Typography>
      
      {/* Filtros */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Buscar componentes"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Tipo de componente</InputLabel>
              <Select
                value={selectedType}
                label="Tipo de componente"
                onChange={(e) => setSelectedType(e.target.value)}
              >
                <MenuItem value="">Todos</MenuItem>
                {componentTypes.map((type) => (
                  <MenuItem key={type} value={type}>{type}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography gutterBottom>
              Rango de precio: ${priceRange[0]} - ${priceRange[1]}
            </Typography>
            <Slider
              value={priceRange}
              onChange={handlePriceChange}
              valueLabelDisplay="auto"
              min={0}
              max={2000}
              step={50}
            />
          </Grid>
        </Grid>
      </Box>
      
      {/* Componentes seleccionados */}
      {selectedComponents.length > 0 && (
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Componentes seleccionados
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {selectedComponents.map((component) => (
              <Chip
                key={component.id}
                label={component.name}
                onDelete={() => handleSelectComponent(component)}
                color="primary"
              />
            ))}
          </Box>
          <Box sx={{ mt: 2 }}>
            <Button 
              variant="contained" 
              color="secondary"
              onClick={() => {
                // Aquí se navegaría a la página de comparación
                console.log('Comparar componentes:', selectedComponents);
              }}
            >
              Comparar seleccionados
            </Button>
          </Box>
        </Box>
      )}
      
      {/* Lista de componentes */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredComponents.length > 0 ? (
            filteredComponents.map((component) => (
              <Grid item key={component.id} xs={12} sm={6} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" component="div" gutterBottom>
                      {component.name}
                    </Typography>
                    <Typography color="text.secondary" gutterBottom>
                      {component.brand} | {component.type}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Rendimiento: {component.performance_score}/100
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Consumo: {component.power_consumption}W
                    </Typography>
                    <Typography variant="h6" color="primary" sx={{ mt: 2 }}>
                      ${component.price.toFixed(2)}
                    </Typography>
                    
                    {/* Especificaciones */}
                    <Box sx={{ mt: 2 }}>
                      {component.specifications.map((spec, index) => (
                        <Typography key={index} variant="body2">
                          <strong>{spec.key}:</strong> {spec.value}
                        </Typography>
                      ))}
                    </Box>
                  </CardContent>
                  <CardActions>
                    <Button 
                      size="small" 
                      color={selectedComponents.some(c => c.id === component.id) ? "secondary" : "primary"}
                      onClick={() => handleSelectComponent(component)}
                    >
                      {selectedComponents.some(c => c.id === component.id) ? "Seleccionado" : "Seleccionar"}
                    </Button>
                    <Button size="small">Ver detalles</Button>
                  </CardActions>
                </Card>
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Typography align="center">
                No se encontraron componentes con los criterios seleccionados.
              </Typography>
            </Grid>
          )}
        </Grid>
      )}
    </Container>
  );
};

export default ComponentSearch;