import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Documents from "./pages/Documents";
import UploadDocument from "./pages/UploadDocument";
import Profile from "./pages/Profile";
import Login from "./pages/Login";
import AdminRoute from "./components/AdminRoute";
import Query from "./pages/Query";
import Register from "./pages/Register";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/documents"
        element={
          <ProtectedRoute>
            <AdminRoute>
              <Documents />
            </AdminRoute>
          </ProtectedRoute>
        }
      />

      <Route
        path="/upload"
        element={
          <ProtectedRoute>
            <AdminRoute>
              <UploadDocument />
            </AdminRoute>
          </ProtectedRoute>
        }
      />

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />

      <Route
        path="/query"
        element={
          <ProtectedRoute>
            <Query />
          </ProtectedRoute>
        }
      />

      <Route path="/register" element={<Register />} />
    </Routes>
  );
}
export default App;
