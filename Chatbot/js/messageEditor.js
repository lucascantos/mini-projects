alert('Yeet');
var sms = [
    {
        categoria: 'Chuva Intensa',
        mensagem: ['Temos alerta de chuva forte entre XXX seguindo para YYY dentro de ZZZ. Isso é causado por AAA. Há risco de rajadas de vento e trovoadas.',
                'Chove forte em XXX e segue em direção à YYY. Essa chuva ocorre por AAA e deve atingir a cidade em ZZZ.',
                'Há registro de Temporais na cidade de XXX causado por AAA. A previsão é que atinja YYY em ZZZ. Não se descarta a possibilidade de ventos fortes e descargas eletricas.',
                ]
    },
    {
        categoria: 'Trovoadas',
        mensagem: ['Agora temos tempestades com raios em XXX. Essas trovoadas devem chegar em YYY nos proximos ZZZ. Essa tempestade ocorre por conta de AAA.',
                'Os ultimos dados mostram descargas eletricas proximas à XXX. Nas proximas ZZZ deve atingir YYY.'
                ]
    },
    {
        categoria: 'Ventania',
        mensagem: ['Alerta de ventania para XXX. Esse vento ocorre por conta de AAA e há risco de novas rajadas nas proximas ZZZ.',
                'Em XXX, foi registrado rajadas de vento acima de 50km/h.',
                'Houve registro de Rajadas de Vento forte em XXX causado pela aproximação de AAA. '
                ]
    }
];
// For eache SMS, Plot h1 de categoria e txt de mensagem
// Pra cada coisa digitada, alterar algo