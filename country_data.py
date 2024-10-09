'''MY: 1
US: 2
GB: 3
DE: 4
CA: 5
AU: 6
FI: 7
ES: 8
ID: 9
NO: 10
GR: 11
IN: 12
BR: 13
AR: 14
IT: 15
PT: 16
HU: 17
IE: 18
RS: 19
CZ: 20
MX: 21
FR: 22
RO: 23
PL: 24
SG: 25
PH: 26
AT: 27
SE: 28
NZ: 29
ZA: 30
DK: 32
JM: 33
PK: 34
HK: 35
HR: 36
AE: 37
TR: 38
RU: 39
EG: 40
SA: 41
CH: 42
BN: 43
JP: 44'''

country_mapping = {
    1: 'Malaysia',
    2: 'United States of America',
    3: 'United Kingdom',
    4: 'Germany',
    5: 'Canada',
    6: 'Australia',
    7: 'Finland',
    8: 'Spain',
    9: 'Indonesia',
    10: 'Norway',
    11: 'Greece',
    12: 'India',
    13: 'Brazil',
    14: 'Argentina',
    15: 'Italy',
    16: 'Portugal',
    17: 'Hungary',
    18: 'Ireland',
    19: 'Serbia',
    20: 'Czechia',
    21: 'Mexico',
    22: 'France',
    23: 'Romania',
    24: 'Poland',
    25: 'Singapore',
    26: 'Philippines',
    27: 'Austria',
    28: 'Sweden',
    29: 'New Zealand',
    30: 'South Africa',
    32: 'Denmark',
    33: 'Jamaica',
    34: 'Pakistan',
    35: 'Hong Kong',
    36: 'Croatia',
    37: 'United Arab Emirates',
    38: 'Turkey',
    39: 'Russia',
    40: 'Egypt',
    41: 'Saudi Arabia',
    42: 'Switzerland',
    43: 'Brunei Darussalam',
    44: 'Japan'
}


country_coords = {
    'Malaysia': [4.2105, 101.9758],
    'United States': [37.0902, -95.7129],
    'United Kingdom': [55.3781, -3.4360],
    'Germany': [51.1657, 10.4515],
    'Estonia': [59.4370, 24.7535],
    'Canada': [56.1304, -106.3468],
    'Ecuador': [-1.8312, -78.1834],
    'Australia': [-25.2744, 133.7751],
    'Finland': [61.9241, 25.7482],
    'Spain': [40.4637, -3.7492],
    'Indonesia': [-0.7893, 113.9213],
    'Dominican Republic': [18.7357, -70.1627],
    'Norway': [60.4720, 8.4689],
    'Greece': [39.0742, 21.8243],
    'India': [20.5937, 78.9629],
    'Sri Lanka': [7.8731, 80.7718],
    'Brazil': [-14.2350, -51.9253],
    'Argentina': [-38.4161, -63.6167],
    'Cambodia': [12.5657, 104.9910],
    'Italy': [41.8719, 12.5674],
    'North Macedonia': [41.6086, 21.7453],
    'Portugal': [39.3999, -8.2245],
    'Bosnia and Herzegovina': [43.9159, 17.6791],
    'Hungary': [47.1625, 19.5033],
    'South Korea': [35.9078, 127.7669],
    'Ireland': [53.4129, -8.2439],
    'Serbia': [44.0165, 21.0059],
    'Czech Republic': [49.8175, 15.4730],
    'Mexico': [23.6345, -102.5528],
    'France': [46.6034, 1.8883],
    'Romania': [45.9432, 24.9668],
    'Poland': [51.9194, 19.1451],
    'Singapore': [1.3521, 103.8198],
    'Philippines': [12.8797, 121.7740],
    'Austria': [47.5162, 14.5501],
    'Ukraine': [48.3794, 31.1656],
    'Colombia': [4.5709, -74.2973],
    'Georgia': [42.3154, 43.3569],
    'Sweden': [60.1282, 18.6435],
    'New Zealand': [-40.9006, 174.8860],
    'South Africa': [-30.5595, 22.9375],
    'Netherlands': [52.1326, 5.2913],
    'Denmark': [56.2639, 9.5018],
    'Jamaica': [18.1096, -77.2975],
    'Chile': [-35.6751, -71.5430],
    'Israel': [31.0461, 34.8516],
    'Pakistan': [30.3753, 69.3451],
    'Nepal': [28.3949, 84.1240],
    'Hong Kong': [22.3964, 114.1095],
    'Croatia': [45.1, 15.2],
    'United Arab Emirates': [23.4241, 53.8478],
    'Turkey': [38.9637, 35.2433],
    'Venezuela': [6.4238, -66.5897],
    'Bulgaria': [42.7339, 25.4858],
    'Peru': [-9.1900, -75.0152],
    'Ghana': [7.4595, -0.5207],
    'Russia': [61.5240, 105.3188],
    'Puerto Rico': [18.2208, -66.5901],
    'Slovenia': [46.1512, 14.9955],
    'Latvia': [56.8796, 24.6032],
    'Albania': [41.1533, 20.1683],
    'Vietnam': [14.0583, 108.2772],
    'Bangladesh': [23.6858, 90.3563],
    'Thailand': [15.8700, 100.9925],
    'Nigeria': [9.0820, 8.6753],
    'Morocco': [31.7917, -7.0926],
    'Faroe Islands': [61.8926, -6.9118],
    'Uruguay': [-32.5228, -55.7658],
    'Egypt': [26.8205, 30.8025],
    'Belgium': [50.8503, 4.3517],
    'Saudi Arabia': [23.8859, 45.0792],
    'El Salvador': [13.7942, -88.8965],
    'Switzerland': [46.8182, 8.2275],
    'Lebanon': [33.8547, 35.8623],
    'Slovakia': [48.6690, 19.6990],
    'Syria': [34.8021, 38.9968],
    'Tunisia': [33.8869, 9.5375],
    'Trinidad and Tobago': [10.6918, -61.2225],
    'Suriname': [3.9193, -56.0278],
    'Kenya': [-0.0236, 37.9062],
    'Panama': [8.9824, -79.5197],
    'Cyprus': [35.1264, 33.2546],
    'Botswana': [-22.3285, 24.6849],
    'Mozambique': [-18.6657, 35.5296],
    'Barbados': [13.1939, -59.5432],
    'Guernsey': [49.4657, -2.5854],
    'Curaçao': [12.1696, -68.9900],
    'Kuwait': [29.3759, 47.9774],
    'Brunei': [4.5353, 114.7277],
    'Maldives': [3.2028, 73.2207],
    'Oman': [21.5126, 55.9233],
    'Algeria': [28.0339, 1.6596],
    'Costa Rica': [9.7489, -83.7534],
    'Iceland': [64.9631, -19.0208],
    'Mauritius': [-20.3484, 57.5522],
    'Moldova': [47.4116, 28.3699],
    'Japan': [36.2048, 138.2529],
    'Guatemala': [15.7835, -90.2308],
    'China': [35.8617, 104.1954],
    'Iran': [32.4279, 53.6880],
    'Lithuania': [55.1694, 23.8813],
    'Montenegro': [42.7087, 19.3744],
    'Nicaragua': [12.8654, -85.2072],
    'Taiwan': [23.6978, 120.9605],
    'Palestine': [31.9474, 35.3026],
    'Jordan': [30.5852, 36.2384],
    'Qatar': [25.3548, 51.1839],
    'Sudan': [12.8628, 30.2176],
    'Cayman Islands': [19.3133, -81.2546],
    'Angola': [-11.2027, 17.8739],
    'Bahamas': [25.0343, -77.3963],
    'Belize': [17.1899, -88.4976],
    'Bolivia': [-16.5000, -68.1193],
    'Paraguay': [-23.4420, -58.4438],
    'Afghanistan': [33.9391, 67.7099],
    'Armenia': [40.0691, 45.0382],
    'Uzbekistan': [41.3775, 64.5853],
    'Guam': [13.4443, 144.7937],
    'Ethiopia': [9.1450, 40.4897],
    'Jersey': [49.2078, -2.1312],
    'Macedonia': [41.6086, 21.7453],
    'Greenland': [71.7069, -42.6043],
    'Nepal': [28.3949, 84.1240],
    'Liberia': [6.4281, -9.4295],
    'Seychelles': [-4.6796, 55.4919],
    'Liechtenstein': [47.1415, 9.5215],
    'San Marino': [43.9333, 12.4500],
    'Liechtenstein': [47.1415, 9.5215],
    'Vatican City': [41.9029, 12.4534],
}

