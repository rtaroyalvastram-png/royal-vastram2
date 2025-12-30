import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import CreateBill from './pages/CreateBill';
import ViewBills from './pages/ViewBills';
import Invoice from './pages/Invoice';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/invoice/:id" element={<Invoice />} />
        <Route path="*" element={
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/create" element={<CreateBill />} />
              <Route path="/bills" element={<ViewBills />} />
            </Routes>
          </Layout>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
