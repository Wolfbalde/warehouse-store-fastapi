import './App.css';
import { BrowserRouter,Routes,Route } from 'react-router-dom';
import { Products } from './routes/Product';
import { Productscreate } from './routes/Productcreate';
import { Order } from './routes/Order';

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Products/>} />
      <Route path="/create" element={<Productscreate/>} />
      <Route path="/order" element={<Order/>} />
    </Routes>
    </BrowserRouter>
  );
}

export default App;
