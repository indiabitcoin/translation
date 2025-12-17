import { useToast } from '../contexts/ToastContext';

export default function Toast() {
  const { toasts, removeToast } = useToast();

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type}`}>
          <div className="toast-content">
            <i
              className={`fas fa-${
                toast.type === 'success'
                  ? 'check-circle'
                  : toast.type === 'error'
                  ? 'exclamation-circle'
                  : toast.type === 'warning'
                  ? 'exclamation-triangle'
                  : 'info-circle'
              }`}
            ></i>
            <span>{toast.message}</span>
          </div>
          <button
            className="toast-close"
            onClick={() => removeToast(toast.id)}
          >
            &times;
          </button>
        </div>
      ))}
    </div>
  );
}
