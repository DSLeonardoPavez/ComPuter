import React, { useState } from 'react';

import {
  Container,
  Typography,
  Box,
  Paper,
  Tabs,
  Tab,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Card,
  CardContent,
  Chip
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

// Datos de ejemplo para desarrollo
const mockComponents = [
  { id: 1, name: 'AMD Ryzen 7 5800X', type: 'CPU', price: 349.99, stock: 15 },
  { id: 2, name: 'NVIDIA GeForce RTX 3080', type: 'GPU', price: 699.99, stock: 5 },
  { id: 3, name: 'Corsair Vengeance RGB Pro 32GB', type: 'RAM', price: 159.99, stock: 20 },
  { id: 4, name: 'Samsung 970 EVO Plus 1TB', type: 'Storage', price: 129.99, stock: 25 },
  { id: 5, name: 'ASUS ROG Strix B550-F Gaming', type: 'Motherboard', price: 189.99, stock: 10 },
];

const mockUsers = [
  { id: 1, name: 'Juan Pérez', email: 'juan@example.com', role: 'user', lastLogin: '2023-05-15' },
  { id: 2, name: 'María López', email: 'maria@example.com', role: 'admin', lastLogin: '2023-05-16' },
  { id: 3, name: 'Carlos Rodríguez', email: 'carlos@example.com', role: 'user', lastLogin: '2023-05-10' },
];

const AdminPanel = () => {
  const [tabValue, setTabValue] = useState(0);
  const [components, setComponents] = useState(mockComponents);
  const [users, setUsers] = useState(mockUsers);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentComponent, setCurrentComponent] = useState({ id: 0, name: '', type: '', price: 0, stock: 0 });
  const [searchTerm, setSearchTerm] = useState('');

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleOpenDialog = (component = { id: 0, name: '', type: '', price: 0, stock: 0 }) => {
    setCurrentComponent(component);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveComponent = () => {
    if (currentComponent.id === 0) {
      // Agregar nuevo componente
      const newComponent = {
        ...currentComponent,
        id: components.length + 1
      };
      setComponents([...components, newComponent]);
    } else {
      // Actualizar componente existente
      setComponents(components.map(comp => 
        comp.id === currentComponent.id ? currentComponent : comp
      ));
    }
    handleCloseDialog();
  };

  const handleDeleteComponent = (id: number) => {
    setComponents(components.filter(comp => comp.id !== id));
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentComponent({
      ...currentComponent,
      [name]: name === 'price' || name === 'stock' ? parseFloat(value) : value
    });
  };

  const handleSelectChange = (e: any) => {
    setCurrentComponent({
      ...currentComponent,
      type: e.target.value
    });
  };

  const filteredComponents = components.filter(comp => 
    comp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    comp.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Panel de Administración
      </Typography>

      <Paper sx={{ width: '100%', mb: 4 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          centered
        >
          <Tab label="Dashboard" />
          <Tab label="Componentes" />
          <Tab label="Usuarios" />
          <Tab label="Configuración" />
        </Tabs>

        {/* Dashboard */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4} >
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Total de Componentes
                  </Typography>
                  <Typography variant="h5" component="div">
                    {components.length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Total de Usuarios
                  </Typography>
                  <Typography variant="h5" component="div">
                    {users.length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Componentes sin Stock
                  </Typography>
                  <Typography variant="h5" component="div">
                    {components.filter(comp => comp.stock === 0).length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Actividad Reciente
                  </Typography>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Acción</TableCell>
                        <TableCell>Usuario</TableCell>
                        <TableCell>Fecha</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        <TableCell>Componente añadido</TableCell>
                        <TableCell>admin@computer.com</TableCell>
                        <TableCell>Hoy, 10:30</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Usuario registrado</TableCell>
                        <TableCell>sistema</TableCell>
                        <TableCell>Hoy, 09:15</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Componentes */}
        <TabPanel value={tabValue} index={1}>
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between' }}>
            <TextField
              label="Buscar componentes"
              variant="outlined"
              size="small"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              sx={{ width: '50%' }}
            />
            <Button
              variant="contained"
              color="primary"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog()}
            >
              Añadir Componente
            </Button>
          </Box>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Nombre</TableCell>
                  <TableCell>Tipo</TableCell>
                  <TableCell>Precio</TableCell>
                  <TableCell>Stock</TableCell>
                  <TableCell>Acciones</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredComponents.map((component) => (
                  <TableRow key={component.id}>
                    <TableCell>{component.id}</TableCell>
                    <TableCell>{component.name}</TableCell>
                    <TableCell>
                      <Chip label={component.type} color="primary" size="small" />
                    </TableCell>
                    <TableCell>${component.price.toFixed(2)}</TableCell>
                    <TableCell>{component.stock}</TableCell>
                    <TableCell>
                      <IconButton size="small" onClick={() => handleOpenDialog(component)}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleDeleteComponent(component.id)}>
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Usuarios */}
        <TabPanel value={tabValue} index={2}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Nombre</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Rol</TableCell>
                  <TableCell>Último acceso</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>{user.id}</TableCell>
                    <TableCell>{user.name}</TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      <Chip 
                        label={user.role} 
                        color={user.role === 'admin' ? 'secondary' : 'default'} 
                        size="small" 
                      />
                    </TableCell>
                    <TableCell>{user.lastLogin}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Configuración */}
        <TabPanel value={tabValue} index={3}>
          <Typography variant="h6" gutterBottom>
            Configuración del Sistema
          </Typography>
          <Box component="form" sx={{ mt: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Nombre del sitio"
                  defaultValue="ComPuter"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Email de contacto"
                  defaultValue="contacto@computer.com"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Descripción del sitio"
                  multiline
                  rows={4}
                  defaultValue="Sistema de recomendación de componentes para PC personalizado"
                />
              </Grid>
              <Grid item xs={12}>
                <Button variant="contained" color="primary">
                  Guardar configuración
                </Button>
              </Grid>
            </Grid>
          </Box>
        </TabPanel>
      </Paper>

      {/* Diálogo para añadir/editar componente */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>
          {currentComponent.id === 0 ? 'Añadir Componente' : 'Editar Componente'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="name"
            label="Nombre del componente"
            type="text"
            fullWidth
            variant="outlined"
            value={currentComponent.name}
            onChange={handleInputChange}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>Tipo de componente</InputLabel>
            <Select
              value={currentComponent.type}
              onChange={handleSelectChange}
              label="Tipo de componente"
            >
              <MenuItem value="CPU">CPU</MenuItem>
              <MenuItem value="GPU">GPU</MenuItem>
              <MenuItem value="RAM">RAM</MenuItem>
              <MenuItem value="Storage">Almacenamiento</MenuItem>
              <MenuItem value="Motherboard">Placa base</MenuItem>
              <MenuItem value="PSU">Fuente de alimentación</MenuItem>
              <MenuItem value="Case">Caja</MenuItem>
              <MenuItem value="Cooling">Refrigeración</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            name="price"
            label="Precio"
            type="number"
            fullWidth
            variant="outlined"
            value={currentComponent.price}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            name="stock"
            label="Stock"
            type="number"
            fullWidth
            variant="outlined"
            value={currentComponent.stock}
            onChange={handleInputChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleSaveComponent} variant="contained" color="primary">
            Guardar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AdminPanel;