<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Todo</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.todo-modal>Add Todo</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col">Is completed</th>
              <th scope="col">Created Date</th>
              <th scope="col">Update Date</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(todo, index) in todos" :key="index">
              <td>{{ todo.title }}</td>
              <td>{{ todo.description }}</td>
              <td>
                <span v-if="todo.is_completed">Yes</span>
                <span v-else>No</span>
              </td>
              <td>{{ dateformat(todo.created_at) }}</td>
              <td>{{ dateformat(todo.updated_at) }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.todo-update-modal
                          @click="editTodo(todo)">
                    Update
                  </button>
                  <button type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteTodo(todo)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTodoModal"
             id="todo-modal"
             title="Add a new Todo"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Title:"
                      label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addTodoForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-description-group"
                      label="Description:"
                      label-for="form-description-input">
          <b-form-input id="form-description-input"
                        type="text"
                        v-model="addTodoForm.description"
                        required
                        placeholder="Enter Description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-is_completed-group">
          <b-form-checkbox-group v-model="addTodoForm.is_completed" id="form-checks">
            <b-form-checkbox value="true">Completed?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editTodoModal"
             id="todo-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                      label="Title:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-description-edit-group"
                      label="Description:"
                      label-for="form-description-edit-input">
          <b-form-input id="form-description-edit-input"
                        type="text"
                        v-model="editForm.description"
                        required
                        placeholder="Enter Description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-is_completed-edit-group">
          <b-form-checkbox-group v-model="editForm.is_completed" id="form-checks">
            <b-form-checkbox value="true">Completed?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
  import axios from 'axios';
  import Alert from './Alert.vue';

  export default {
    data() {
      return {
        todos: [],
        addTodoForm: {
          title: '',
          description: '',
          is_completed: [],
        },
        message: '',
        showMessage: false,
        editForm: {
          id: '',
          title: '',
          description: '',
          is_completed: [],
        },
      };
    },
    components: {
      alert: Alert,
    },
    methods: {
      dateformat(date){
     
      if (date!=null){
      return new Intl.DateTimeFormat('en-US', { dateStyle: 'long' }).format(new Date(date.$date ));
      }
      else{
        
        return "";
      }
      },
      getTodos() {
        const path = 'http://localhost:5000/todos';
        axios.get(path)
          .then((res) => {
            this.todos = res.data.todos;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      addTodo(payload) {
        const path = 'http://localhost:5000/todos';
        axios.post(path, payload)
          .then(() => {
            this.getTodos();
            this.message = 'Todo added!';
            this.showMessage = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getTodos();
          });
      },
      initForm() {
        this.addTodoForm.title = '';
        this.addTodoForm.description = '';
        this.addTodoForm.is_completed = [];
        this.editForm.id = '';
        this.editForm.title = '';
        this.editForm.description = '';
        this.editForm.is_completed = [];
      },
      onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addTodoModal.hide();
        let is_completed = false;
        if (this.addTodoForm.is_completed[0]) is_completed = true;
        const payload = {
          title: this.addTodoForm.title,
          description: this.addTodoForm.description,
          is_completed, 
        };
        this.addTodo(payload);
        this.initForm();
      },
      onReset(evt) {
        evt.preventDefault();
        this.$refs.addTodoModal.hide();
        this.initForm();
      },
      editTodo(todo) {
        this.editForm = todo;
      },
      onSubmitUpdate(evt) {
        evt.preventDefault();
        this.$refs.editTodoModal.hide();
        let is_completed = false;
        if (this.editForm.is_completed[0]) is_completed = true;
        const payload = {
          title: this.editForm.title,
          description: this.editForm.description,
          is_completed,
        };
        const finalData = JSON.parse(JSON.stringify(this.editForm));
        this.updateTodo(payload, finalData._id);
      },
      updateTodo(payload, todoID) {
        const path = `http://localhost:5000/todos/${todoID.$oid}`;
        axios.put(path, payload)
          .then(() => {
            this.getTodos();
            this.message = 'Todo updated!';
            this.showMessage = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.getTodos();
          });
      },
      onResetUpdate(evt) {
        evt.preventDefault();
        this.$refs.editTodoModal.hide();
        this.initForm();
        this.getTodos(); 
      },
      removeTodo(todoID) {
        const path = `http://localhost:5000/todos/${todoID.$oid}`;
        axios.delete(path)
          .then(() => {
            this.getTodos();
            this.message = 'Todo removed!';
            this.showMessage = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.getTodos();
          });
      },
      onDeleteTodo(todo) {
        /* eslint no-underscore-dangle: 0 */
        const finalData = JSON.parse(JSON.stringify(todo));
        this.removeTodo(finalData._id);
      },
    },
    created() {
      this.getTodos();
    },
  };
</script>
