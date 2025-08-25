// Kanban Drag and Drop functionality
document.addEventListener('DOMContentLoaded', function() {
    const taskCards = document.querySelectorAll('.task-card');
    const kanbanColumns = document.querySelectorAll('.kanban-column');
    
    // Add drag event listeners to task cards
    taskCards.forEach(card => {
        card.addEventListener('dragstart', handleDragStart);
        card.addEventListener('dragend', handleDragEnd);
    });
    
    // Add drop event listeners to columns
    kanbanColumns.forEach(column => {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('drop', handleDrop);
        column.addEventListener('dragenter', handleDragEnter);
        column.addEventListener('dragleave', handleDragLeave);
    });
    
    let draggedTask = null;
    
    function handleDragStart(e) {
        draggedTask = this;
        this.style.opacity = '0.5';
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.outerHTML);
    }
    
    function handleDragEnd(e) {
        this.style.opacity = '1';
        draggedTask = null;
    }
    
    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }
    
    function handleDragEnter(e) {
        this.classList.add('drag-over');
    }
    
    function handleDragLeave(e) {
        this.classList.remove('drag-over');
    }
    
    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation();
        }
        
        this.classList.remove('drag-over');
        
        if (draggedTask !== this) {
            const taskId = draggedTask.dataset.taskId;
            const newStatus = this.dataset.status;
            
            // Update task status via API
            fetch(`/api/tasks/${taskId}/status`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: newStatus })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Move the task card to the new column
                    this.appendChild(draggedTask);
                    
                    // Update badge counts
                    updateColumnCounts();
                    
                    // Show success message
                    showMessage('Tarefa movida com sucesso!', 'success');
                } else {
                    showMessage('Erro ao mover tarefa: ' + (data.error || 'Erro desconhecido'), 'danger');
                }
            })
            .catch(error => {
                showMessage('Erro ao mover tarefa: ' + error.message, 'danger');
            });
        }
        
        return false;
    }
    
    function updateColumnCounts() {
        kanbanColumns.forEach(column => {
            const taskCount = column.querySelectorAll('.task-card').length;
            const badge = column.closest('.card').querySelector('.badge');
            if (badge) {
                badge.textContent = taskCount;
            }
        });
    }
    
    function showMessage(message, type) {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1050; max-width: 400px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
});

// CSS for drag and drop visual feedback
const style = document.createElement('style');
style.textContent = `
    .drag-over {
        background-color: var(--bs-light) !important;
        border: 2px dashed var(--bs-primary) !important;
    }
    
    .task-card {
        cursor: move;
        transition: all 0.2s ease;
    }
    
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
`;
document.head.appendChild(style);
