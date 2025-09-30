🎨 AppWeb Pink-World

Aplicação web desenvolvida como parte do Projeto Integrador em Computação I da Univesp. Destinada ao gerenciamento de clientes e serviços, com foco em atender às necessidades de pequenos empreendimentos. Como demonstração prática da solução proposta, foi criada uma aplicação personalizada para o salão de beleza Pink World.

✨ Funcionalidades

📅 Agendamento de serviços

👥 Cadastro e gerenciamento de clientes

🧾 Controle de serviços prestados

📊 Visualização de relatórios

🛠️ Interface simples e intuitiva

🛠️ Tecnologias Utilizadas

Backend: Python 3.13.2 com Flask

Frontend: HTML, CSS (sem frameworks externos)

Banco de Dados: SQLite (via SQLAlchemy)

Variáveis de Ambiente: python-dotenv

📂 Estrutura do Projeto
AppWeb_Pink-World/
├── templates/               # Páginas HTML

├── static/                  # Arquivos estáticos (CSS, JS, imagens)

├── instance/                # Configurações locais

├── app.py                   # Aplicação principal Flask

├── requirements.txt         # Dependências do projeto

└── README.md                # Este arquivo

⚙️ Como Executar

Clone o repositório:

git clone https://github.com/Allanizepi/AppWeb_Pink-World.git
cd AppWeb_Pink-World


Crie e ative um ambiente virtual:

python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate


Instale as dependências:

pip install -r requirements.txt


Execute a aplicação:

python app.py


Acesse a aplicação em http://127.0.0.1:5000/.


Nota: O envio de e-mails pode não funcionar corretamente em ambientes de desenvolvimento devido a restrições de segurança.

🚀 Melhorias Futuras

🔐 Implementação de autenticação de usuários

📱 Desenvolvimento de versão mobile responsiva

📈 Integração com APIs de pagamento

🌐 Deploy em plataformas como Heroku ou Render

👤 Autor

Allan Izepi
GitHub: Allanizepi

LinkedIn: Allan Izepi
