import axios, { AxiosResponse, AxiosError } from 'axios';

// Configuración base de Axios
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export { API_URL };
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requests - agregar token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses - manejo de errores globales
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Interfaces
export interface ISpecification {
  id: number;
  name: string;
  value: string;
  unit?: string;
}

export interface IComponent {
  id: number;
  name: string;
  type: string;
  brand: string;
  model: string;
  price: number;
  currency: string;
  availability: boolean;
  image_url?: string;
  description?: string;
  specifications: ISpecification[];
  performance_score?: number;
  power_consumption?: number;
  release_date?: string;
  warranty_months?: number;
  rating?: number;
  reviews_count?: number;
}

export interface ICompatibilityCheck {
  component1_id: number;
  component2_id: number;
}

export interface ICompatibilityResult {
  compatible: boolean;
  score: number;
  issues: string[];
  recommendations?: string[];
}

export interface IRecommendationRequest {
  user_profile: {
    budget: number;
    use_case: string;
    experience_level: string;
    preferences?: {
      brand_preferences?: string[];
      performance_priority?: string;
      noise_tolerance?: string;
      rgb_preference?: boolean;
    };
  };
  existing_components?: number[];
  component_types?: string[];
}

export interface IRecommendationResponse {
  recommendations: IComponent[];
  total_price: number;
  compatibility_score: number;
  performance_rating: string;
  explanation: string;
  alternatives?: IComponent[];
}

export interface IUserProfile {
  id: number;
  username: string;
  email: string;
  budget: number;
  use_case: string;
  experience_level: string;
  preferences: any;
  created_at: string;
  updated_at: string;
}

export interface ISearchFilters {
  type?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
  search_term?: string;
  sort_by?: 'price' | 'performance' | 'rating' | 'name';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

export interface IPaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
  per_page: number;
}

// Funciones de la API

// Componentes
export const getComponents = async (filters?: ISearchFilters): Promise<IPaginatedResponse<IComponent>> => {
  try {
    const response = await api.get('/components', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Error fetching components:', error);
    throw error;
  }
};

export const getComponent = async (id: number): Promise<IComponent> => {
  try {
    const response = await api.get(`/components/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching component ${id}:`, error);
    throw error;
  }
};

export const getComponentsByType = async (type: string): Promise<IComponent[]> => {
  try {
    const response = await api.get(`/components/type/${type}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching components by type ${type}:`, error);
    throw error;
  }
};

export const searchComponents = async (
  searchTerm: string,
  filters?: Omit<ISearchFilters, 'search_term'>
): Promise<IPaginatedResponse<IComponent>> => {
  try {
    const response = await api.get('/components/search', {
      params: { search_term: searchTerm, ...filters }
    });
    return response.data;
  } catch (error) {
    console.error('Error searching components:', error);
    throw error;
  }
};

// Compatibilidad
export const checkCompatibility = async (
  componentIds: number[]
): Promise<ICompatibilityResult> => {
  try {
    const response = await api.post('/compatibility/check', {
      component_ids: componentIds
    });
    return response.data;
  } catch (error) {
    console.error('Error checking compatibility:', error);
    throw error;
  }
};

export const checkPairCompatibility = async (
  component1Id: number,
  component2Id: number
): Promise<ICompatibilityResult> => {
  try {
    const response = await api.post('/compatibility/check-pair', {
      component1_id: component1Id,
      component2_id: component2Id
    });
    return response.data;
  } catch (error) {
    console.error('Error checking pair compatibility:', error);
    throw error;
  }
};

// Recomendaciones
export const getRecommendations = async (
  request: IRecommendationRequest
): Promise<IRecommendationResponse> => {
  try {
    const response = await api.post('/recommendations', request);
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

export const getSmartRecommendations = async (
  budget: number,
  useCase: string,
  existingComponents?: number[]
): Promise<IRecommendationResponse> => {
  try {
    const response = await api.post('/recommendations/smart', {
      budget,
      use_case: useCase,
      existing_components: existingComponents
    });
    return response.data;
  } catch (error) {
    console.error('Error getting smart recommendations:', error);
    throw error;
  }
};

// Perfil de usuario
export const getUserProfile = async (): Promise<IUserProfile> => {
  try {
    const response = await api.get('/user/profile');
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const updateUserProfile = async (profile: Partial<IUserProfile>): Promise<IUserProfile> => {
  try {
    const response = await api.put('/user/profile', profile);
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

export const createUserProfile = async (profile: Omit<IUserProfile, 'id' | 'created_at' | 'updated_at'>): Promise<IUserProfile> => {
  try {
    const response = await api.post('/user/profile', profile);
    return response.data;
  } catch (error) {
    console.error('Error creating user profile:', error);
    throw error;
  }
};

// Autenticación
export const login = async (username: string, password: string): Promise<{ access_token: string; token_type: string }> => {
  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};

export const register = async (
  username: string,
  email: string,
  password: string
): Promise<IUserProfile> => {
  try {
    const response = await api.post('/auth/register', {
      username,
      email,
      password
    });
    return response.data;
  } catch (error) {
    console.error('Error registering:', error);
    throw error;
  }
};

export const logout = (): void => {
  localStorage.removeItem('token');
  window.location.href = '/';
};

// Estadísticas y métricas
export const getComponentStats = async (): Promise<any> => {
  try {
    const response = await api.get('/stats/components');
    return response.data;
  } catch (error) {
    console.error('Error fetching component stats:', error);
    throw error;
  }
};

export const getPopularComponents = async (limit: number = 10): Promise<IComponent[]> => {
  try {
    const response = await api.get(`/stats/popular-components?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching popular components:', error);
    throw error;
  }
};

// Comparación de componentes
export const compareComponents = async (componentIds: number[]): Promise<any> => {
  try {
    const response = await api.post('/components/compare', {
      component_ids: componentIds
    });
    return response.data;
  } catch (error) {
    console.error('Error comparing components:', error);
    throw error;
  }
};

// Obtener recomendaciones de componentes
export const getComponentRecommendations = async (request: {
  budget: number;
  use_case: string;
  component_types: string[];
}): Promise<any> => {
  try {
    const response = await api.post('/components/recommendations', request);
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

// Ejecutar scraper
export const runScraper = async (componentTypes?: string[]): Promise<any> => {
  try {
    const response = await api.post('/scraper/run', {
      component_types: componentTypes
    });
    return response.data;
  } catch (error) {
    console.error('Error running scraper:', error);
    throw error;
  }
};



// Precios y ofertas
export const getPriceHistory = async (componentId: number, days: number = 30): Promise<any> => {
  try {
    const response = await api.get(`/components/${componentId}/price-history?days=${days}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching price history:', error);
    throw error;
  }
};

export const getBestDeals = async (limit: number = 20): Promise<IComponent[]> => {
  try {
    const response = await api.get(`/deals/best?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching best deals:', error);
    throw error;
  }
};

// Utilidades
export const healthCheck = async (): Promise<{ status: string; timestamp: string }> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking API health:', error);
    throw error;
  }
};

export default api;