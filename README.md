# Gerenciador de Tarefas

Este é um **Gerenciador de Tarefas** simples, desenvolvido com **Flask** e **SQLAlchemy**. O sistema permite que os usuários façam login, cadastrem novas tarefas, editem, concluam e excluam tarefas. Além disso, oferece funcionalidades de **filtros de pesquisa** e **paginamento** para facilitar a visualização e organização das tarefas.

## Funcionalidades

- **Cadastro de Usuários**: Crie uma conta com nome de usuário e senha.
- **Login e Logout**: Realize login para acessar o sistema e logout quando terminar.
- **Gerenciamento de Tarefas**: Adicione, edite, conclua ou exclua tarefas.
- **Filtros de Pesquisa**: Filtre as tarefas por **status** e **prazo** (atrasadas, vencendo em 7 dias, etc.).
- **Paginamento**: Navegue pelas páginas de tarefas com um número limitado de tarefas por página.
- **Segurança**: Senhas são armazenadas de forma segura utilizando **hashing**.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **SQLAlchemy**: ORM para gerenciar o banco de dados.
- **Flask-Login**: Gerenciamento de sessões de login.
- **Werkzeug**: Utilizado para hash de senhas.

## Como Usar

### 1. **Cadastro de Usuário**
   - Na página de **Cadastro**, insira um **nome de usuário** e uma **senha**.
   - A senha deve ter **pelo menos 6 caracteres**.
   - Após preencher os campos, clique em **Cadastrar** para criar a conta.

### 2. **Login**
   - Acesse a página de **Login** com seu **nome de usuário** e **senha**.
   - Caso o login seja bem-sucedido, você será redirecionado para a página principal com a lista de **tarefas**.

### 3. **Página de Tarefas**
   - Na página principal, você pode **visualizar, editar, concluir ou excluir tarefas**.
   - **Filtros de Pesquisa**: Você pode filtrar as tarefas por **status** (Pendente ou Concluída) e **prazo** (Tarefas Atrasadas ou Vencendo em 7 dias).
   - As tarefas serão exibidas paginadas, ou seja, somente um número limitado de tarefas será mostrado por vez.

### 4. **Adicionando Tarefas**
   - Clique no botão **Adicionar Tarefa** para criar novas tarefas.
   - Preencha os campos **Título**, **Descrição**, **Prazo** e **Categoria** e clique em **Salvar**.

### 5. **Editando Tarefas**
   - Clique no botão **Editar** ao lado de uma tarefa para alterar seu **Título**, **Descrição**, **Prazo** ou **Categoria**.

### 6. **Concluindo Tarefas**
   - Clique no botão **Concluir** para marcar uma tarefa como concluída. Isso altera o **status** da tarefa para "Concluída", e ela aparecerá com um fundo verde na lista.

### 7. **Excluindo Tarefas**
   - Clique no botão **Deletar** para excluir permanentemente uma tarefa.

### 8. **Logout**
   - Após terminar de usar o sistema, clique em **Sair** para finalizar a sessão e sair da sua conta.

## Contribuindo

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades! Siga os passos abaixo:

1. Faça um **fork** deste repositório.
2. Crie uma nova branch:
   ```bash
   git checkout -b minha-nova-funcionalidade
3. Faça suas alterações e commite:
git commit -am 'Adicionando nova funcionalidade

4. Push para sua branch:
   git push origin minha-nova-funcionalidade
   
5.Abra um pull request explicando as mudanças que você fez.

