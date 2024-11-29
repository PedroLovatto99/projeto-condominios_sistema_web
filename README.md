</head>
<body>
  <h1>Condomínio Manager</h1>
  <p><strong>Condomínio Manager</strong> é um sistema web desenvolvido com Django para o gerenciamento do condomínio residencial do <strong>Recanto Maestro</strong>. O sistema permite que administradores realizem cadastro, edição, remoção e visualização de blocos, apartamentos e residentes, podendo gerar tabelas Excel das informações de um bloco específico ou de todos os blocos para fins de controle do histórico de mudanças. O sistema possui autenticação baseada em níveis de acesso para garantir que informações confidenciais sejam exibidas apenas a usuários autorizados.</p>

  <h2>Funcionalidades</h2>
  <ul>
    <li><strong>Gerenciamento de Blocos:</strong> Cadastro, visualização, edição e exclusão de blocos residenciais.</li>
    <li><strong>Gerenciamento de Apartamentos:</strong> Controle detalhado de apartamentos pertencentes a cada bloco.</li>
    <li><strong>Gerenciamento de Residentes:</strong> Cadastro de residentes com informações como nome, telefone e histórico de ocupação.</li>
    <li><strong>Controle de Acesso:</strong>
      <ul>
        <li><strong>Usuário Administrador:</strong> Possui acesso total ao sistema, podendo visualizar, editar e excluir todas as informações.</li>
        <li><strong>Usuário Convidado:</strong> Tem acesso limitado, podendo visualizar apenas informações básicas dos blocos e apartamentos, sem detalhes sensíveis dos residentes.</li>
      </ul>
    </li>
  </ul>

  <h2>Tecnologias Utilizadas</h2>
  <ul>
    <li><strong>Back-end:</strong> Django</li>
    <li><strong>Banco de Dados:</strong> PostgreSQL</li>
    <li><strong>Autenticação:</strong> Sistema de autenticação do Django</li>
    <li><strong>Front-end:</strong> Templates do Django</li>
  </ul>

</body>
